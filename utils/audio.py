# -*- coding: utf-8 -*-

from .playlist import Playlist


def get_player(ctx):
    try:
        player = ctx.bot.players[str(ctx.guild.id)]
    except KeyError:
        ctx.bot.players[str(ctx.guild.id)] = Playlist()
        player = ctx.bot.players[str(ctx.guild.id)]
    return player
