# -*- coding: utf-8 -*-

import asyncio


class Playlist:
    def __init__(self, ctx):
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()
        self.ctx = ctx

        self.song = None
        self.loop = ctx.bot.loop.create_task(self.playlist())

    def clear(self):
        self.queue._queue.clear()

    async def add(self, source):
        await self.queue.put(source)

    async def play(self):
        self.ctx.voice_client.play(
            self.song,
            after=lambda _: self.ctx.bot.loop.call_soon_threadsafe(self.next.set),
        )

        await self.ctx.send(
            ":musical_note: Now playing: **{0.uploader}** - **{0.title}**.".format(
                self.song
            )
        )

    async def playlist(self):
        await self.ctx.bot.wait_until_ready()
        while not self.ctx.bot.is_closed():
            self.next.clear()
            self.song = await self.queue.get()

            await self.play()
            await self.next.wait()

            self.song.cleanup()
            self.song = None

            if len(self.queue._queue) == 0:
                await self.ctx.voice_client.disconnect()
                del self.ctx.bot.players[str(self.ctx.guild.id)]
                await self.ctx.send(":information_source: End of the playlist.")
