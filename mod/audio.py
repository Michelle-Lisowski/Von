# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import asyncio
import functools
from functools import partial

import discord
import youtube_dl
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
    "source_address": "0.0.0.0"
}

ffmpegopts = {
    "before_options": "-nostdin",
    "options": "-vn"
}

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
    async def create_source(cls, ctx, search: str, *, loop=None, download=False):
        loop = loop or asyncio.get_event_loop()
        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)
        playlist = ctx.cog.players[str(ctx.guild.id)]

        if "entries" in data:
            data = data["entries"][0]

        if playlist.current:
            await ctx.send(
                f":information_source: **{data['uploader']}** - **"
                f"{data['title']}** has been added to the playlist."
            )
        return cls(discord.FFmpegPCMAudio(data['url'], **ffmpegopts), data=data, requester=ctx.author)


class Playlist:
    def __init__(self, ctx):
        self.bot = ctx.bot
        self.guild = ctx.guild
        self.channel = ctx.channel

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.current = None
        self.volume = 0.5
        
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
                    self.guild.voice_client.play(self.current, after=lambda n: self.bot.loop.call_soon_threadsafe(self.next.set))
                    await self.channel.send(
                        f":musical_note: Now playing: **{self.current.uploader}"
                        f"** - **{self.current.title}**"
                    )
                    await self.next.wait()

            source.cleanup()
            self.current = None

            if self.current is None:
                if len(self.queue._queue) < 1:
                    await self.guild.voice_client.disconnect()
                    await self.channel.send(":information_source: End of the playlist.")


class Audio:
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    def get_playlist(self, ctx):
        try:
            playlist = self.players[str(ctx.guild.id)]
        except KeyError:
            playlist = Playlist(ctx)
            self.players[str(ctx.guild.id)] = playlist
        return playlist

    @commands.command()
    async def play(self, ctx, *, search: str = None):
        if search is None:
            await ctx.send(":grey_exclamation: Please specify a search query.")
            return

        if not ctx.voice_client:
            if not ctx.author.voice:
                await ctx.send(":grey_exclamation: Please join a voice channel.")
            else:
                await ctx.author.voice.channel.connect()
        
        async with ctx.typing():
            playlist = self.get_playlist(ctx)
            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            await playlist.add(source)

    @commands.command()
    async def playfirst(self, ctx, *, search: str = None):
        if search is None:
            await ctx.send(":grey_exclamation: Please specify a search query.")
            return

        if not ctx.voice_client:
            if not ctx.author.voice:
                await ctx.send(":grey_exclamation: Please join a voice channel.")
            else:
                await ctx.author.voice.channel.connect()

        async with ctx.typing():
            playlist = self.get_playlist(ctx)
            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            await playlist.add_first(source)

    @commands.command()
    async def skip(self, ctx):
        if not ctx.voice_client:
            await ctx.send(":grey_exclamation: No music is currently playing.")
            return
        ctx.voice_client.stop()

    @commands.command()
    async def clear(self, ctx):
        if not ctx.voice_client:
            await ctx.send(":grey_exclamation: No music is currently playing.")
            return

        playlist = self.get_playlist(ctx)
        await playlist.clear()
        await ctx.send(":white_check_mark: Playlist cleared.")

    @commands.command()
    async def stop(self, ctx):
        if not ctx.voice_client:
            await ctx.send(":grey_exclamation: No music is currently playing.")
            return

        playlist = self.get_playlist(ctx)
        playlist.player.cancel()

        await ctx.voice_client.disconnect()
        await ctx.send(f":information_source: Music stopped by **{ctx.author.name}**.")


def setup(bot):
    bot.add_cog(Audio(bot))
