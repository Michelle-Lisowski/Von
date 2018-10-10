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
import time
import traceback
from functools import partial

import discord
from async_timeout import timeout
from discord import opus, utils
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
    'source_address': '0.0.0.0'
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)

with open('guilds.json', 'r') as fp:
    guilds = json.load(fp)

def literal_duration(duration):
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    
    duration = []
    if seconds < 10:
        seconds = f'0{seconds}'

    if hours > 0:
        duration.append(str(hours))
    duration.append(str(minutes))
    duration.append(str(seconds))

    return ':'.join(duration)

class VoiceConnectionError(commands.CommandError):
    pass

class InvalidVoiceChannel(VoiceConnectionError):
    pass

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester
        self.title = data.get('title')
        self.duration = data.get('duration')
        self.uploader = data.get('uploader')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False, repeat=False):
        loop = loop or asyncio.get_event_loop()
        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]

        if repeat:
            pass
        else:
            duration = literal_duration(data['duration'])
            await ctx.send(f":information_source: **{data['uploader']}** - **{data['title']} ({duration})** has been added to the playlist.")

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title'], 'uploader': data['uploader']}
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
            duration = literal_duration(self.current.duration)

            if self._guild.voice_client:
                if not self._guild.voice_client.is_playing():
                    self._guild.voice_client.play(self.current, after=lambda n: self.bot.loop.call_soon_threadsafe(self.next.set))
                    await self._channel.send(f':musical_note: Now playing: **{self.current.uploader}** - **{self.current.title} ({duration})**')
                    await self.next.wait()

            source.cleanup()
            self.current = None

            if self.current is None:
                if len(self.queue._queue) == 0:
                    self.end(self._guild)
                    await self._channel.send(':information_source: End of the playlist.')

    def end(self, guild):
        self.bot.loop.create_task(self._cog.stop(guild))

class Music:
    __slots__ = ('bot', 'players', 'task')
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.task = None

    async def stop(self, guild):
        if not guild.voice_client:
            pass
        else:
            await guild.voice_client.disconnect()

        try:
            del self.players[str(guild.id)]
        except KeyError:
            pass

    def get_player(self, ctx):
        try:
            player = self.players[str(ctx.guild.id)]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[str(ctx.guild.id)] = player
        return player

    async def repeat_on(self, ctx):
        player = self.get_player(ctx)
        search = str(player.current.title)
        player.current = None

        while player.current is None:
            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False, repeat=True)
            await player.queue.put(source)
        time.sleep(1)

    async def repeat_off(self, ctx):
        player = self.get_player(ctx)
        if self.task is None:
            return

        self.task.cancel()
        self.task = None
        player.queue._queue.clear()            

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

        elif isinstance(error, commands.CommandInvokeError):
            if str(ctx.command) == 'volume':
                await ctx.send(f":sound: Current volume level: **{round(guilds[str(ctx.guild.id)]['DEFAULT_VOLUME'] * 100)}%**")

        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send(error)

        elif isinstance(error, VoiceConnectionError):
            await ctx.send(error)

        elif isinstance(error, AttributeError):
            print(f'Missing voice client in guild \'{str(ctx.guild)}\'')

        else:
            print(f'Ignoring exception in guild \'{str(ctx.guild)}\', command \'{str(ctx.command)}\':', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command()
    @commands.guild_only()
    async def connect(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel(':grey_exclamation: Please join a voice channel or specify one for me to join.')

        vc = ctx.voice_client
        if vc:
            if vc.channel.id == channel.id:
                await ctx.send(f':information_source: Current voice channel: **{vc.channel.name}**')
            elif vc.is_playing():
                await ctx.send(f':information_source: You can\'t move me to a different channel when music is playing.')
            else:
                try:
                    await vc.move_to(channel)
                    await ctx.send(f':information_source: Moved to voice channel **{channel}**.')
                except asyncio.TimeoutError:
                    raise VoiceConnectionError(f':x: Moving to voice channel **{channel}** timed out.')
        else:
            try:
                if channel:
                    await channel.connect(reconnect=True)
                    await ctx.send(f':information_source: Connected to voice channel **{channel}**.')
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f':x: Connecting to voice channel **{channel}** timed out.')

    @commands.command()
    @commands.guild_only()
    async def play(self, ctx, *, search: str = None):
        vc = ctx.voice_client
        if search is None:
            await ctx.send(':grey_exclamation: Please specify a search query.')
        elif not ctx.author.voice:
            if vc:
                await ctx.send(f':grey_exclamation: Please join me in the voice channel **{vc.channel}**.')
            else:
                await ctx.send(':grey_exclamation: Please join a voice channel first.')
        elif vc and ctx.author.voice.channel != vc.channel:
            await ctx.send(f':grey_exclamation: Please join me in the voice channel **{vc.channel}**.')      
        else:
            async with ctx.typing():
                if not vc:
                    await ctx.invoke(self.connect)
                    player = self.get_player(ctx)
                    source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
                    await player.queue.put(source)
                else:
                    player = self.get_player(ctx)
                    if self.task:
                        await self.repeat_off(ctx)
                        player.queue._queue.clear()
                    source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
                    await player.queue.put(source)

    @commands.command()
    @commands.guild_only()
    async def pause(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        elif not ctx.author.voice or ctx.author.voice.channel != vc.channel:
            await ctx.send(f':grey_exclamation: Please join me in the voice channel **{vc.channel}**.')
        elif vc.is_paused():
            await ctx.send(':grey_exclamation: The current song has already been paused.')
        else:
            vc.pause()
            await ctx.send(f':pause_button: Song paused by **{ctx.author.name}**.')

    @commands.command(aliases=['unpause', 'continue'])
    @commands.guild_only()
    async def resume(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        elif not ctx.author.voice or ctx.author.voice.channel != vc.channel:
            await ctx.send(f':grey_exclamation: Please join me in the voice channel **{vc.channel}**.')
        elif not vc.is_paused():
            await ctx.send(':grey_exclamation: The current song was never paused.')
        else:
            vc.resume()
            await ctx.send(f':arrow_forward: Song resumed by **{ctx.author.name}**.')

    @commands.command()
    @commands.guild_only()
    async def skip(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        elif not vc.is_playing():
            await ctx.send(':grey_exclamation: No music is currently playing.')
        else:
            if not len(vc.channel.members) >= 3:
                if not ctx.author.voice or ctx.author.voice.channel != vc.channel:
                    await ctx.send(f':grey_exclamation: Please join me in the voice channel **{vc.channel}**.')
                else:
                    vc.stop()
                    await ctx.send(f':information_source: Song skipped by **{ctx.author.name}**.')
                return

            embed = discord.Embed()
            embed.title = 'Jaffa'
            embed.description = '**Decide whether or not to skip the currently playing song!**'
            embed.colour = 0x0099ff
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

    @commands.command(aliases=['queue', 'upcoming'])
    @commands.guild_only()
    async def playlist(self, ctx):
        vc = ctx.voice_client
        player = self.get_player(ctx)

        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        elif len(player.queue._queue) == 0:
            await ctx.send(':grey_exclamation: There are currently no queued songs.')
        else:
            upcoming = list(itertools.islice(player.queue._queue, 0, 5))
            fmt = '\n'.join(f"**{u['uploader']}** - **{u['title']}**" for u in upcoming)
            embed = discord.Embed()
            embed.title = f'Upcoming - Next {len(upcoming)} Songs'
            embed.description = fmt
            embed.colour = 0x0099ff
            await ctx.send(embed=embed)

    @commands.command(aliases=['now_playing'])
    @commands.guild_only()
    async def np(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        elif not vc.is_playing():
            await ctx.send(':grey_exclamation: No music is currently playing.')
        else:
            player = self.get_player(ctx)
            if not player.current:
                await ctx.send(':grey_exclamation: No music is currently playing.')
            else:
                duration = literal_duration(player.current.duration)
                await ctx.send(f':musical_note: Now playing: **{player.current.uploader}** - **{player.current.title} ({duration})**')

    @commands.command()
    @commands.guild_only()
    async def clear(self, ctx):
        vc = ctx.voice_client
        player = self.get_player(ctx)

        if not vc.is_playing():
            await ctx.send(':grey_exclamation: No music is currently playing.')
        elif player.queue.empty():
            await ctx.send(':grey_exclamation: There are currently no queued songs.')
        else:
            if not len(vc.channel.members) >= 3:
                if not ctx.author.voice or ctx.author.voice.channel != vc.channel:
                    await ctx.send(f':grey_exclamation: Please join me in the voice channel **{vc.channel}**.')
                else:
                    if self.task:
                        await self.repeat_off(ctx)
                    player.queue._queue.clear()
                    await ctx.send(':information_source: Playlist successfully cleared.')
                return

            embed = discord.Embed()
            embed.title = 'Jaffa'
            embed.description = '**Decide whether or not to clear the current playlist!**'
            embed.colour = 0x0099ff
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
                player.queue._queue.clear()
                await ctx.send(':information_source: Vote ended and playlist cleared.')
                await cache_msg.clear_reactions()                

    @commands.command()
    @commands.guild_only()
    async def repeat(self, ctx):
        vc = ctx.voice_client
        player = self.get_player(ctx)

        if not vc.is_playing():
            await ctx.send(':grey_exclamation: No music is currently playing.')
        elif not ctx.author.voice:
            await ctx.send(f':grey_exclamation: Please join me in the voice channel **{vc.channel}**.')
        else:
            if ctx.author.voice.channel != vc.channel:
                await ctx.send(f':grey_exclamation: Please join me in the voice channel **{vc.channel}**.')
                return

            if not self.task:
                player.queue._queue.clear()
                self.task = self.bot.loop.create_task(self.repeat_on(ctx))
                await ctx.send(':repeat_one: Song repetition enabled.')
            else:
                await self.repeat_off(ctx)
                player.queue._queue.clear()
                await ctx.send(':repeat_one: Song repetition disabled.')

    @commands.command(name='stop')
    @commands.guild_only()
    async def stop_command(self, ctx):
        vc = ctx.voice_client
        player = self.get_player(ctx)

        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        else:
            if not len(vc.channel.members) >= 3:
                if not ctx.author.voice or ctx.author.voice.channel != vc.channel:
                    await ctx.send(f':grey_exclamation: Please join me in the voice channel **{vc.channel}**.')
                else:
                    if self.task:
                        await self.repeat_off(ctx)
                    player.queue._queue.clear()
                    await self.stop(ctx.guild)
                return

            embed = discord.Embed()
            embed.title = 'Jaffa'
            embed.description = '**Decide whether or not to stop the current playlist!**'
            embed.colour = 0x0099ff
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
                if self.task:
                    player.queue._queue.clear()
                await self.stop(ctx.guild)
                await cache_msg.clear_reactions()

    @commands.command()
    @commands.guild_only()
    async def volume(self, ctx, *, volume: int = None):
        vc = ctx.voice_client
        player = self.get_player(ctx)

        if not vc or not vc.is_connected():
            await ctx.send(':grey_exclamation: I\'m currently not connected to a voice channel.')
        elif volume is None:
            await ctx.send(f':sound: Current volume level: **{round(vc.source.volume * 100)}%**.')
        elif ctx.author.voice.channel != vc.channel:
            await ctx.send(f':grey_exclamation: Please join me in the voice channel **{vc.channel}**.')
        elif not 0 < volume < 101:
            await ctx.send(':grey_exclamation: Please specify a number between `1` and `100`.')
        else:
            if vc.source:
                vc.source.volume = (volume / 100)
            player.volume = (volume / 100)
            await ctx.send(f':sound: New volume level: **{volume}%**.')

def setup(bot):
    bot.add_cog(Music(bot))
