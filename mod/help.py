# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

from .settings import Settings


class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *, command: str = None):
        help_cmds = ["help", "modules", "cmds"]
        owner_cmds = ["load", "unload", "reload"]

        cmd = self.bot.get_command(command)
        prefix = self.bot.prefixes[str(ctx.guild.id)]["prefix"]

        if command is None:
            embed = discord.Embed()
            embed.title = self.bot.user.name
            embed.colour = 0x0099FF

            embed.description = (
                "`v!cmds [module]` returns a list of commands in the "
                "specified module.\n`v!modules` returns a list of available "
                "command modules.\n~~`v!help [command]` returns information "
                "about the specified command.~~"
            )

            if ctx.guild:
                await ctx.send(":mailbox_with_mail: Check your DMs")
            await ctx.author.send(embed=embed)
        elif cmd is None:
            await ctx.send("Command not found.")
        else:
            if command in help_cmds or command in owner_cmds:
                await ctx.invoke(self.help)
                return

            embed = discord.Embed()
            embed.colour = 0x0099FF
            embed.description = f"**{cmd.description}**"

            if len(cmd.qualified_name.split(" ")) > 1:
                embed.title = f"{cmd.cog_name}: {cmd.name.title().replace('_', ' ')}"
            else:
                embed.title = cmd.name.capitalize()

            embed.add_field(name="Usage", value=f"`{prefix}{cmd.usage}`")
            embed.add_field(name="Example", value=f"`{prefix}{cmd.brief}`")

            embed.set_footer(
                text="{argument} - optional argument; [argument] - required argument"
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def modules(self, ctx):
        embed = discord.Embed()
        embed.title = "Command Modules"
        embed.colour = 0x0099FF
        mods = []

        for mod in self.bot.cogs:
            if mod == "Owner":
                continue
            else:
                mods.append(mod)

        mods = "\n".join(mods)
        embed.description = mods
        await ctx.send(embed=embed)

    @commands.command()
    async def cmds(self, ctx, module: str = None):
        if module is None:
            await ctx.invoke(self.modules)
            return

        if module.lower() == "owner":
            await ctx.invoke(self.modules)
            return

        if module.lower() == "settings":
            subcmds = Settings(self.bot).settings
            await ctx.invoke(subcmds)
            return

        mod = self.bot.get_cog(module.capitalize())
        if mod is None:
            await ctx.invoke(self.modules)
            return

        embed = discord.Embed()
        embed.title = f"{module.capitalize()} Commands"
        embed.colour = 0x0099FF

        try:
            prefix = self.bot.prefixes[str(ctx.guild.id)]["prefix"]
        except:
            prefix = "v!"
        cmds = []

        for cmd in self.bot.get_cog_commands(module.capitalize()):
            cmds.append(prefix + cmd.qualified_name)

        cmds = "` `".join(cmds)
        embed.description = f"**`{cmds}`**"
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
