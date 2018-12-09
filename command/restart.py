# -*- coding: utf-8 -*-

import os
import sys

from discord.ext import commands


@commands.command()
async def restart(ctx):
    process = ctx.bot.process
    for handler in process.open_files() + process.connections():
        os.close(handler.fd)
    os.execl(sys.executable, sys.executable, *sys.argv)


def setup(bot):
    bot.add_command(restart)
