# -*- coding: utf-8 -*-

import asyncio
import random


class Playlist:
    def __init__(self, ctx):
        self.channel = ctx.channel
        self.client = ctx.voice_client
        self.guild = ctx.guild
        self.bot = ctx.bot

        self.entries = asyncio.Queue()
        self.next = asyncio.Event()

        self.loop = self.bot.loop.create_task(self.playlist())
        self.entry = None

    def cleanup(self):
        self.entry = None
        self.loop.cancel()

        del self.bot.players[str(self.guild.id)]
        self.bot.loop.create_task(self.client.disconnect())

    def clear(self):
        self.entries._queue.clear()

    def put(self, entry, *, first=False):
        if first is True:
            self.entries._queue.appendleft(entry)
        else:
            self.entries._queue.append(entry)

    def shuffle(self):
        random.shuffle(self.entries._queue)

    async def get(self):
        while self.entries is not None:
            if len(self.entries._queue) > 0:
                return self.entries._queue.popleft()
            await asyncio.sleep(0.25)

    async def play(self):
        entry = await self.get()
        self.client.play(entry, after=lambda _: self.next.set())

        self.entry = entry
        await self.channel.send(
            ":musical_note: Now playing: **{0.uploader}** - **{0.title}**".format(
                self.entry
            )
        )

    async def playlist(self):
        while not self.bot.is_closed():
            self.next.clear()
            await self.play()
            await self.next.wait()

            if len(self.entries._queue) == 0:
                self.cleanup()
                await self.channel.send(":information_source: End of the playlist.")
