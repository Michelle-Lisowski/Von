# -*- coding: utf-8 -*-

import asyncio


class Playlist:
    def __init__(self, ctx):
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()
        self.ctx = ctx

        self.song = None
        self.loop = ctx.bot.loop.create_task(self.play())

    async def play(self):
        pass
