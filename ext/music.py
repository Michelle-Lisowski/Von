"""
The MIT License (MIT)

Copyright (c) 2018 sirtezza451

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import asyncio
import datetime
import json
import itertools
import sys
import traceback
from functools import partial

import discord
from async_timeout import timeout
from discord import opus, utils
from discord.ext import commands
from youtube_dl import YoutubeDL

from main import handler, logger

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
    'source_address': '0.0.0.0'
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)

with open('guilds.json', 'r') as fp:
    guilds = json.load(fp)

class VoiceConnectionError(commands.CommandError):
    pass

class InvalidVoiceChannel(VoiceConnectionError):
    pass

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
    __slots__ = ('bot', '_guild', '_command', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')
    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._command = ctx.command
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None
        self.current = None
        self.volume = guilds[str(self._guild.id)]['DEFAULT_VOLUME']
        self.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.next.clear()
            if not self._guild.voice_client:
                return

            try:
                async with timeout(300):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                self.end(self._guild)

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

            self._guild.voice_client.play(source, after=lambda n: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f':musical_note: Now playing: **{source.title}**.')
            await self.next.wait()

            source.cleanup()
            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

            if self.current is None and len(self.queue._queue) == 0:
                self.end(self._guild)
                await self._channel.send(':information_source: End of the playlist.')
                return

    def end(self, guild):
        self.bot.loop.create_task(self._cog.stop(guild))
        return

class Music:
    __slots__ = ('bot', 'players')
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def stop(self, guild):
        if not guild.voice_client:
            return
        else:
            await guild.voice_client.disconnect()

        try:
            del self.players[str(guild.id)]
        except KeyError:
            pass

    async def __error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.send(':x: This command can\'t be used in private messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if str(ctx.command) == 'connect':
                await ctx.send(':x: I could not find that voice channel.')
            elif str(ctx.command) == 'volume':
                await ctx.send(':x: Please specify a **whole number** for the volume.')

        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send(error)

        elif isinstance(error, VoiceConnectionError):
            await ctx.send(error)

        elif isinstance(error, AttributeError):
            # print(f'Missing voice client in guild \'{str(ctx.guild)}\'')
            logger.warning(f'Missing voice client in guild \'{str(ctx.guild)}\'')

        else:
            # print(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':', file=sys.stderr)
            # traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            logger.warning(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':')
            logger.error(traceback.format_exc())

    def get_player(self, ctx):
        try:
            player = self.players[str(ctx.guild.id)]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[str(ctx.guild.id)] = player
        return player

    @commands.command(name='connect')
    @commands.guild_only()
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel(':grey_exclamation: Please join a voice channel or specify one for me to join.')

        vc = ctx.voice_client
        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
                await ctx.send(f':information_source: Moved to voice channel **{channel}**.')
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f':x: Moving to voice channel **{channel}** timed out.')
        else:
            try:
                await channel.connect(reconnect=True)
                await ctx.send(f':information_source: Connected to voice channel **{channel}**.')
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f':x: Connecting to voice channel **{channel}** timed out.')

    @commands.command(name='play')
    @commands.guild_only()
    async def play_(self, ctx, *, search: str = None):
        if search is None:
            await ctx.send(':grey_exclamation: Please specify a search query.')
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
        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        elif not ctx.author.voice:
            await ctx.send(f':grey_exclamation: Please join me in the voice channel **{ctx.voice_client.channel}**.')
        elif vc.is_paused():
            await ctx.send(':grey_exclamation: The current song has already been paused.')
        else:
            vc.pause()
            await ctx.send(f':pause_button: Song paused by **{ctx.author.name}**.')

    @commands.command(name='resume', aliases=['unpause'])
    @commands.guild_only()
    async def resume_(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        elif not ctx.author.voice:
            await ctx.send(f':grey_exclamation: Please join me in the voice channel **{ctx.voice_client.channel}**.')
        elif not vc.is_paused():
            await ctx.send(':grey_exclamation: The current song was never paused.')
        else:
            vc.resume()
            await ctx.send(f':musical_note: Song resumed by **{ctx.author.name}**.')

    @commands.command(name='skip')
    @commands.guild_only()
    async def skip_(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        elif not vc.is_playing():
            await ctx.send(':grey_exclamation: No music is currently playing.')
        else:
            if not len(vc.channel.members) >= 3:
                vc.stop()
                await ctx.send(f':information_source: Song skipped by **{ctx.author.name}**.')
                return

            embed = discord.Embed()
            embed.title = 'Procbot'
            embed.description = '**Decide whether or not to skip the currently playing song!**'
            embed.colour = 0x0000ff
            embed.set_footer(text='You have 15 seconds to vote.')
            bot_msg = await ctx.send(embed=embed)

            await bot_msg.add_reaction('👍')
            await bot_msg.add_reaction('👎')
            await asyncio.sleep(15)

            cache_msg = await ctx.get_message(bot_msg.id)
            thumbs_up = utils.get(cache_msg.reactions, emoji='👍')
            thumbs_down = utils.get(cache_msg.reactions, emoji='👎')

            if not thumbs_up.count > thumbs_down.count:
                await ctx.send(':information_source: Vote ended and song continued.')
                await cache_msg.clear_reactions()
            else:
                vc.stop()
                await ctx.send(':information_source: Vote ended and song skipped.')
                await cache_msg.clear_reactions()

    @commands.command(name='playlist', aliases=['queue', 'upcoming'])
    @commands.guild_only()
    async def playlist_(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        else:
            player = self.get_player(ctx)
            if player.queue.empty():
                await ctx.send(':grey_exclamation: There are currently no queued songs.')
                return

            upcoming = list(itertools.islice(player.queue._queue, 0, 5))
            fmt = '\n'.join(f"**{u['title']}**" for u in upcoming)
            embed = discord.Embed()
            embed.title = f'Upcoming - Next {len(upcoming)} Songs'
            embed.description = fmt
            embed.colour = 0x0000ff
            await ctx.send(embed=embed)

    @commands.command(name='np', aliases=['now_playing'])
    @commands.guild_only()
    async def now_playing_(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        elif not vc.is_playing():
            await ctx.send(':grey_exclamation: No music is currently playing.')
        else:
            player = self.get_player(ctx)
            if not player.current:
                await ctx.send(':grey_exclamation: No music is currently playing.')

            try:
                await player.np.delete()
            except discord.HTTPException:
                pass
            player.np = await ctx.send(f':musical_note: Now playing: **{vc.source.title}**.')

    @commands.command(name='stop')
    @commands.guild_only()
    async def stop_(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        else:
            if not len(vc.channel.members) >= 3:
                await self.stop(ctx.guild)
                return

            embed = discord.Embed()
            embed.title = 'Procbot'
            embed.description = '**Decide whether or not to stop the current playlist!**'
            embed.colour = 0x0000ff
            embed.set_footer(text='You have 15 seconds to vote.')
            bot_msg = await ctx.send(embed=embed)

            await bot_msg.add_reaction('👍')
            await bot_msg.add_reaction('👎')
            await asyncio.sleep(15)

            cache_msg = await ctx.get_message(bot_msg.id)
            thumbs_up = utils.get(cache_msg.reactions, emoji='👍')
            thumbs_down = utils.get(cache_msg.reactions, emoji='👎')

            if not thumbs_up.count > thumbs_down.count:
                await ctx.send(':information_source: Vote ended and playlist continued.')
                await cache_msg.clear_reactions()
            else:
                await self.stop(ctx.guild)
                await cache_msg.clear_reactions()

    @commands.command(name='volume')
    @commands.guild_only()
    async def volume_(self, ctx, *, volume: int = None):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        elif volume is None:
            await ctx.send(f':sound: Current volume level: **{round(vc.source.volume * 100)}%**.')
        elif not ctx.author.voice:
            await ctx.send(f':grey_exclamation: Please join me in the voice channel **{ctx.voice_client.channel}**.')
        elif not 0 < volume < 101:
            await ctx.send(':grey_exclamation: Please specify a number between `1` and `100`.')
        else:
            player = self.get_player(ctx)
            if vc.source:
                vc.source.volume = (volume / 100)
            player.volume = (volume / 100)
            await ctx.send(f':sound: New volume level: **{volume}%**.')

def setup(bot):
    bot.add_cog(Music(bot))
