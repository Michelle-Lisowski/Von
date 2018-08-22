import datetime
import json

import discord
from discord import utils
from discord.ext import commands

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason: str = None):
        with open('mod_logs.json', 'r') as fp:
            mod_logs = json.load(fp)

        if member is None:
            await ctx.send(':no_entry_sign: You didn\'t mention a member to be muted!')
            return
        elif member.id == ctx.author.id:
            await ctx.send(':no_entry_sign: Why would you want to mute yourself?')
            return
        elif member.id == self.bot.user.id:
            await ctx.send(':no_entry_sign: I can\'t mute myself! Why would you want to mute me anyway?')
            return
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(':no_entry_sign: You can\'t mute someone with a role equal to or higher than yours!')
            return
        else:
            role = utils.get(ctx.guild.roles, name='Muted')
            if role in member.roles:
                await ctx.send(f':no_entry_sign: **{member.name}** has already been muted!')
                return
            else:
                if reason is None:
                    reason = 'No reason given.'

                await member.add_roles(role)
                embed = discord.Embed()
                embed.title = ':zipper_mouth: Member Muted'
                embed.colour = 0x0000ff
                embed.add_field(name='Member Name', value=member.name, inline=False)
                embed.add_field(name='Member ID', value=member.id, inline=False)
                embed.add_field(name='Muted By', value=ctx.author.name, inline=False)
                embed.add_field(name='Reason', value=reason, inline=False)
                embed.set_footer(text=datetime.datetime.now())
                await ctx.send(embed=embed)

                mod_logs[str(ctx.guild.id)]['MUTE_CASES'] += 1
                with open('mod_logs.json', 'w') as fp:
                    json.dump(mod_logs, fp, indent=4)
                await self.bot.on_mute(author=ctx.author, member=member, reason=str(reason))

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(':no_entry_sign: You didn\'t mention a member to be unmuted!')
            return
        elif member.id == ctx.author.id:
            await ctx.send(':no_entry_sign: How would you be able to unmute yourself if you\'re not muted?')
            return
        elif member.id == self.bot.user.id:
            await ctx.send(':no_entry_sign: I can\'t be muted, so how can I be unmuted?')
            return
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(':no_entry_sign: You can\'t unmute someone with a role equal to or higher than yours!')
            return
        else:
            role = utils.get(ctx.guild.roles, name='Muted')
            if not role in member.roles:
                await ctx.send(f':no_entry_sign: **{member.name}** was never muted!')
                return
            else:
                await member.remove_roles(role)
                embed = discord.Embed()
                embed.title = ':open_mouth: Member Unmuted'
                embed.colour = 0x0000ff
                embed.add_field(name='Member Name', value=member.name, inline=False)
                embed.add_field(name='Member ID', value=member.id, inline=False)
                embed.add_field(name='Unmuted By', value=ctx.author.name, inline=False)
                embed.set_footer(text=datetime.datetime.now())
                await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int = None):
        if number is None:
            await ctx.send(':no_entry_sign: You didn\'t specify a number of messages to be deleted!')
            return
        elif number > 100:
            await ctx.send(f':no_entry_sign: `{number}` isn\'t a valid number! Please specify a number between 2 and 100.')
            return
        elif number < 2:
            await ctx.send(f':no_entry_sign: `{number}` isn\'t a valid number! Please specify a number between 2 and 100.')
            return
        else:
            purged = await ctx.channel.purge(limit=number, check=None)
            embed = discord.Embed()
            embed.title = ':white_check_mark: Success!'
            embed.description = f'Successfully deleted **{len(purged)}** messages.'
            embed.colour = 0x00ff00
            embed.set_footer(text=datetime.datetime.now())
            await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
