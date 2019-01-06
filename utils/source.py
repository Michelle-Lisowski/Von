# -*- coding: utf-8 -*-

import asyncio

import discord
import youtube_dl

from .audio import get_player

youtube_dl.utils.bug_reports_message = lambda: ""

ytdlopts = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": True,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

ffmpegopts = {"options": "-vn"}
downloader = youtube_dl.YoutubeDL(ytdlopts)


class Source(discord.PCMVolumeTransformer):
    def __init__(self, source, *, volume, data):
        super().__init__(source, volume)

        self.url = data.get("url")
        self.title = data.get("title")
        self.uploader = data.get("uploader")

    @classmethod
    async def download(cls, ctx, search: str, *, loop=None, volume=None, stream=False):
        player = get_player(ctx)
        volume = volume or 0.5
        loop = loop or asyncio.get_event_loop()

        data = await loop.run_in_executor(
            None, lambda: downloader.extract_info(search, download=not stream)
        )

        if "entries" in data:
            data = data["entries"][0]
        source = data["url"] if stream else downloader.prepare_filename(data)

        if player.entry is not None:
            await ctx.send(
                ":musical_note: **{}** - **{}** has been added to the playlist.".format(
                    data["uploader"], data["title"]
                )
            )

        return cls(
            discord.FFmpegPCMAudio(source, **ffmpegopts), volume=volume, data=data
        )
