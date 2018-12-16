# -*- coding: utf-8 -*-


def get_player(ctx):
    try:
        player = ctx.bot.players[str(ctx.guild.id)]
    except KeyError:
        ctx.bot.players[str(ctx.guild.id)] = None
        player = ctx.bot.players[str(ctx.guild.id)]
    return player
