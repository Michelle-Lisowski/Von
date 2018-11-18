# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import asyncio
import functools
import random
from functools import partial

import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

ytdlopts = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

ffmpegopts = {"before_options": "-nostdin", "options": "-vn"}

ytdl = YoutubeDL(ytdlopts)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester
        self.title = data.get("title")
        self.duration = data.get("duration")
        self.uploader = data.get("uploader")
        self.url = data.get("webpage_url")

    @classmethod
    async def create_source(
        cls, ctx, search: str, *, loop=None, download=False, repeat=False
    ):
        loop = loop or asyncio.get_event_loop()
        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)
        playlist = ctx.cog.players[str(ctx.guild.id)]

        if "entries" in data:
            data = data["entries"][0]

        if playlist.current:
            if not repeat:
                await ctx.send(
                    f":musical_note: **{data['uploader']}** - **"
                    f"{data['title']}** has been added to the playlist."
                )
        return cls(
            discord.FFmpegPCMAudio(data["url"], **ffmpegopts),
            data=data,
            requester=ctx.author,
        )


class Playlist:
    def __init__(self, ctx):
        self.bot = ctx.bot
        self.guild = ctx.guild
        self.channel = ctx.channel
        self.command = ctx.command
        self.cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.current = None
        self.volume = 0.5

        self.repeat = False
        self.player = self.bot.loop.create_task(self.loop())

    async def add(self, source):
        await self.queue.put(source)

    async def add_first(self, source):
        try:
            self.queue._queue.insert(0, source)
        except IndexError:
            await self.queue.put(source)

    async def clear(self):
        self.queue._queue.clear()

    async def shuffle(self):
        random.shuffle(self.queue._queue)

    async def loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            if not self.guild.voice_client:
                return

            self.next.clear()
            source = await self.queue.get()

            source.volume = self.volume
            self.current = source

            if self.guild.voice_client:
                if not self.guild.voice_client.is_playing():
                    self.guild.voice_client.play(
                        self.current,
                        after=lambda n: self.bot.loop.call_soon_threadsafe(
                            self.next.set
                        ),
                    )
                    await self.channel.send(
                        ":musical_note: Now playing: **{0.uploader}** - **{0.title}**".format(
                            self.current
                        )
                    )
                    await self.next.wait()

                source.cleanup()
                self.current = None

            if self.current is None and self.cog.task is None:
                if len(self.queue._queue) < 1:
                    if self.command.qualified_name != "stop":
                        await self.guild.voice_client.disconnect()
                        await self.channel.send("End of the playlist.")
                        del self.cog.players[str(self.guild.id)]


class Audio:
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.task = None

    def get_playlist(self, ctx):
        try:
            playlist = self.players[str(ctx.guild.id)]
        except KeyError:
            playlist = Playlist(ctx)
            self.players[str(ctx.guild.id)] = playlist
        return playlist

    async def repeat_song(self, ctx):
        playlist = self.get_playlist(ctx)
        search = str(playlist.current.title)
        playlist.repeat = True

        while playlist.repeat is True:
            source = await YTDLSource.create_source(
                ctx, search, loop=self.bot.loop, download=False, repeat=True
            )
            await playlist.add_first(source)

    async def __error(self, ctx, error):
        error = getattr(error, "original", error)

        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command can't be used in private messages.")

        elif isinstance(error, commands.CommandError):
            await ctx.send(error)

    @commands.command()
    @commands.guild_only()
    async def play(self, ctx, *, search: str = None):
        async with ctx.typing():
            playlist = self.get_playlist(ctx)
            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            await playlist.add(source)

    @commands.command()
    @commands.guild_only()
    async def playfirst(self, ctx, *, search: str = None):
        async with ctx.typing():
            playlist = self.get_playlist(ctx)
            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            await playlist.add_first(source)

    @commands.command()
    @commands.guild_only()
    async def pause(self, ctx):
        playlist = self.get_playlist(ctx)

        if playlist.current is None:
            await ctx.send("No music is currently playing.")
        elif ctx.voice_client.is_paused():
            await ctx.send("The current song has already been paused.")
        else:
            ctx.voice_client.pause()
            await ctx.send(":pause_button: Song paused.")

    @commands.command()
    @commands.guild_only()
    async def resume(self, ctx):
        playlist = self.get_playlist(ctx)

        if playlist.current is None:
            await ctx.send("No music is currently playing.")
        elif ctx.voice_client.is_playing():
            await ctx.send("The current song was never paused.")
        else:
            ctx.voice_client.resume()
            await ctx.send(":musical_note: Song resumed.")

    @commands.command()
    @commands.guild_only()
    async def current(self, ctx):
        playlist = self.get_playlist(ctx)

        if playlist.current is None:
            await ctx.send("No music is currently playing.")
        else:
            await ctx.send(
                ":musical_note: Currently playing: **{0.uploader}** - **{0.title}**".format(
                    playlist.current
                )
            )

    @commands.command()
    @commands.guild_only()
    async def peek(self, ctx):
        playlist = self.get_playlist(ctx)

        if playlist.current is None:
            await ctx.send("No music is currently playing.")
        elif len(playlist.queue._queue) < 1:
            await ctx.send("No songs are currently queued.")
        else:
            await ctx.send(
                ":musical_note: Next song: **{0.uploader}** - **{0.title}**".format(
                    list(playlist.queue._queue)[0]
                )
            )

    @commands.command()
    @commands.guild_only()
    async def playlist(self, ctx):
        playlist = self.get_playlist(ctx)

        if playlist.current is None:
            await ctx.send("No music is currently playing.")
        elif len(playlist.queue._queue) < 1:
            await ctx.send("No songs are currently queued.")
        else:
            if playlist.repeat is True:
                await ctx.send(
                    ":repeat_one: Repetition is enabled for: **{0.uploader}** - **{0.title}**".format(
                        playlist.current
                    )
                )
            else:
                embed = discord.Embed()
                embed.colour = 0x0099FF

                songs = []
                position = 0

                for entry in list(playlist.queue._queue):
                    position += 1
                    songs.append(
                        "**{0}:** **{1.uploader}** - **{1.title}**".format(
                            position, entry
                        )
                    )

                if len(playlist.queue._queue) == 1:
                    title = "Current Playlist - 1 Song"
                else:
                    title = f"Current playlist - {len(playlist.queue._queue)} Songs"
                description = "\n".join(songs)

                embed.title = title
                embed.description = description
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def volume(self, ctx, volume: int = None):
        playlist = self.get_playlist(ctx)

        if playlist.current is None:
            await ctx.send("No music is currently playing.")
        elif volume is None:
            volume = round(playlist.current.volume * 100)
            await ctx.send(f":sound: Current volume level: **{volume}%**.")
        elif not 0 < volume < 101:
            await ctx.send("Please specify a number between 1 and 100.")
        else:
            if volume == 100:
                volume = 1.0
            elif volume < 10:
                volume = float(f"0.0{volume}")
            else:
                volume = float(f"0.{volume}")

            async with ctx.typing():
                while playlist.current.volume < volume:
                    playlist.current.volume += 0.01
                    await asyncio.sleep(0.05)

                while playlist.current.volume > volume:
                    playlist.current.volume -= 0.01
                    await asyncio.sleep(0.05)
                await ctx.send(
                    f":sound: Volume level set to **{round(volume * 100)}%**."
                )

    @commands.command()
    @commands.guild_only()
    async def skip(self, ctx):
        playlist = self.get_playlist(ctx)

        if playlist.current is None:
            await ctx.send("No music is currently playing.")
            return
        ctx.voice_client.stop()

    @commands.command()
    @commands.guild_only()
    async def clear(self, ctx):
        playlist = self.get_playlist(ctx)

        if playlist.current is None:
            await ctx.send("No music is currently playing.")
            return

        await playlist.clear()
        await ctx.send(":white_check_mark: Playlist cleared.")

    @commands.command()
    @commands.guild_only()
    async def repeat(self, ctx):
        playlist = self.get_playlist(ctx)

        if playlist.current is None:
            await ctx.send("No music is currently playing.")
            return

        if self.task is not None:
            self.task.cancel()
            self.task = None

            playlist.repeat = False
            repeats = [
                entry
                for entry in list(playlist.queue._queue)
                if entry.title == playlist.current.title
                and entry.uploader == playlist.current.uploader
            ]

            for entry in repeats:
                playlist.queue._queue.remove(entry)
            await ctx.send(":repeat_one: Repetition disabled.")
        else:
            self.task = self.bot.loop.create_task(self.repeat_song(ctx))
            await ctx.send(":repeat_one: Repetition enabled.")

    @commands.command()
    @commands.guild_only()
    async def shuffle(self, ctx):
        playlist = self.get_playlist(ctx)

        if playlist.current is None:
            await ctx.send("No music is currently playing.")
            return

        random.shuffle(playlist.queue._queue)
        await ctx.send(":white_check_mark: Playlist shuffled.")

    @commands.command()
    @commands.guild_only()
    async def stop(self, ctx):
        playlist = self.get_playlist(ctx)

        if playlist.current is None:
            await ctx.send("No music is currently playing.")
            return

        playlist.player.cancel()
        del self.players[str(ctx.guild.id)]

        await ctx.voice_client.disconnect()
        await ctx.send(f"Music stopped by **{ctx.author.name}**.")

    @play.before_invoke
    @playfirst.before_invoke
    @shuffle.before_invoke
    @repeat.before_invoke
    @pause.before_invoke
    @resume.before_invoke
    @volume.before_invoke
    async def voice_check(self, ctx):
        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                raise commands.CommandError("Please join a voice channel first.")
        elif not ctx.author.voice:
            raise commands.CommandError("Please join a voice channel first.")
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            channel = ctx.voice_client.channel
            raise commands.CommandError(
                f"Please join me in the voice channel **{channel}**."
            )


def setup(bot):
    bot.add_cog(Audio(bot))
