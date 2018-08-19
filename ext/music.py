# Procbot.music by sirtezza_451
import asyncio
import datetime
import itertools
import sys
import traceback
from functools import partial

import discord
from async_timeout import timeout
from discord import opus
from discord.ext import commands
from youtube_dl import YoutubeDL

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)

class VoiceConnectionError(commands.CommandError):
    '''Custom Exception class for connection errors.'''

class InvalidVoiceChannel(VoiceConnectionError):
    '''Exception for cases of invalid voice channels.'''

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester
        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()
        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]

        await ctx.send(f":information_source: **{data['title']}** has been added to the queue.")

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}
        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)
        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)

class MusicPlayer:
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')
    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None
        self.volume = 0.5
        self.current = None
        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.next.clear()
            try:
                async with timeout(300):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    embed = discord.Embed()
                    embed.title = ':x: Error!'
                    embed.description = f'```{e}```'
                    embed.colour = 0xff0000
                    embed.set_footer(text=datetime.datetime.now())
                    await self._channel.send(embed=embed)
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f':musical_note: Now playing: **{source.title}**')
            await self.next.wait()

            source.cleanup()
            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))

class Music:
    __slots__ = ('bot', 'players')
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send(':no_entry_sign: This command can\'t be used in private messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, InvalidVoiceChannel):
            return await ctx.send(':information_source: Error connecting to voice channel. Please make sure you are in a valid voice channel.')

        elif isinstance(error, commands.UserInputError):
            embed = discord.Embed()
            embed.title = ':x: Error!'
            embed.description = f'```{error}```'
            embed.colour = 0xff0000
            embed.set_footer(text=f'This will be logged | {datetime.datetime.now()}')
            print(f'Exception in guild: {ctx.guild.name}:')
            print(error, bold=True)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed()
            embed.title = ':x: Error!'
            embed.description = f'```{error}```'
            embed.colour = 0xff0000
            embed.set_footer(text=f'This will be logged | {datetime.datetime.now()}')
            print(f'Exception in guild: {ctx.guild.name}:')
            print(error, bold=True)
            await ctx.send(embed=embed)

        else:
            print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player
        return player

    @commands.command(name='connect')
    @commands.guild_only()
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel(':information_source: No channel to join. Please join a valid channel or specify the name of one.')
        
        vc = ctx.voice_client
        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
                await ctx.send(f':information_source: Moved to **{channel}**')
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f':information_source: Moving to **{channel}** timed out.')
        else:
            try:
                await channel.connect(reconnect=True)
                await ctx.send(f':information_source: Connected to **{channel}**')
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f':information_source: Connecting to **{channel}** timed out.')

    @commands.command(name='play')
    @commands.guild_only()
    async def play_(self, ctx, *, search: str = None):
        if search is None:
            return await ctx.send(':information_source: You didn\'t specify a search query!')
        else:
            async with ctx.typing():
                vc = ctx.voice_client
                if not vc:
                    await ctx.invoke(self.connect_)
                    player = self.get_player(ctx)
                    source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
                    await player.queue.put(source)
                else:
                    player = self.get_player(ctx)
                    source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
                    await player.queue.put(source)

    @commands.command(name='pause')
    @commands.guild_only()
    async def pause_(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_playing():
            return await ctx.send(':information_source: No music is currently playing!')
        elif vc.is_paused():
            return await ctx.send(':information_source: Music has already been paused!')
        else:
            vc.pause()
            await ctx.send(f':information_source: Music paused by **{ctx.author.name}**')

    @commands.command(name='resume')
    @commands.guild_only()
    async def resume_(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send(':information_source: I\'m not connected to a voice channel!')
        elif not vc.is_paused():
            return await ctx.send(':information_source: Music was never paused!')
        else:
            vc.resume()
            await ctx.send(f':information_source: Music resumed by **{ctx.author.name}**')

    @commands.command(name='skip')
    @commands.guild_only()
    async def skip_(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send(':information_source: I\'m not connected to a voice channel!')
        elif not vc.is_playing():
            return await ctx.send(':information_source: No music is currently playing!')
        else:
            vc.stop()
            await ctx.send(f':information_source: Song skipped by **{ctx.author.name}**')

    @commands.command(name='playlist')
    @commands.guild_only()
    async def queue_info(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send(':information_source: I\'m not connected to a voice channel!')
        else:
            player = self.get_player(ctx)
            if player.queue.empty():
                return await ctx.send(':information_source: There are currently no queued songs.')

            upcoming = list(itertools.islice(player.queue._queue, 0, 5))
            fmt = '\n'.join(f"**{_['title']}**" for _ in upcoming)
            embed = discord.Embed()
            embed.title = f'Upcoming - Next {len(upcoming)} Songs'
            embed.description = fmt
            embed.colour = 0x0000ff
            await ctx.send(embed=embed)

    @commands.command(name='np')
    @commands.guild_only()
    async def now_playing_(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send(':information_source: I\'m not connected to a voice channel!')
        elif not vc.is_playing():
            return await ctx.send(':information_source: No music is currently playing!')
        else:
            player = self.get_player(ctx)
            if not player.current:
                return await ctx.send(':information_source: No music is currently playing!')
            try:
                await player.np.delete()
            except discord.HTTPException:
                pass
            player.np = await ctx.send(f':information_source: Now playing: **{vc.source.title}**')

    @commands.command(name='stop')
    @commands.guild_only()
    async def stop_(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send(':information_source: I\'m not connected to a voice channel!')
        else:
            await self.cleanup(ctx.guild)
            await ctx.send(f':information_source: Music stopped by **{ctx.author.name}**')

    @commands.command(name='volume')
    @commands.guild_only()
    async def volume_(self, ctx, *, volume: int = None):
        vc = ctx.voice_client
        cv = ctx.voice_client.source.volume
        if volume is None:
            return await ctx.send(f':sound: Current volume level: **{round(cv * 100)}%**')
        elif not vc or not vc.is_connected():
            return await ctx.send(':information_source: I\'m not connected to a voice channel!')
        elif not 0 < volume < 101:
            return await ctx.send(':information_source: Please specify a value between `1` and `100`')
        else:
            player = self.get_player(ctx)
            if vc.source:
                vc.source.volume = volume / 100
            player.volume = volume / 100
            await ctx.send(f':sound: Volume level set to: **{volume}%**')

def setup(bot):
    bot.add_cog(Music(bot))
