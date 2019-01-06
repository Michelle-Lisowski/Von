# -*- coding: utf-8 -*-

import asyncio
import random


class Playlist:
    def __init__(self, ctx):
        self.client = ctx.voice_client
        self.bot = ctx.bot
        self.ctx = ctx

        self.entries = asyncio.Queue()
        self.next = asyncio.Event()

        self.loop = self.bot.loop.create_task(self.playlist())
        self.entry = None

    def cleanup(self):
        self.loop.cancel()
        del self.bot.players[str(self.ctx.guild.id)]
        self.bot.loop.create_task(self.client.disconnect())

    def clear(self):
        self.entries._queue.clear()

    def put(self, entry, *, first=False):
        if first is True:
            self.entries._queue.appendleft(entry)
        else:
            self.entries._queue.append(entry)

        self.entries._unfinished_tasks += 1
        self.entries._finished.clear()
        self.entries._wakeup_next(self.entries._getters)

    def shuffle(self):
        random.shuffle(self.entries._queue)

    async def play(self):
        self.entry = await self.entries.get()
        self.client.play(self.entry, after=lambda _: self.next.set())

        await self.ctx.send(
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
                await self.ctx.send(":information_source: End of the playlist.")
