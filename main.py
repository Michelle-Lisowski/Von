# Procbot Copyright (C) 2018 sirtezza451
# The full license can be found at master/LICENSE

import datetime
import json
import os
import random
import time
import traceback
from os import listdir
from os.path import isfile, join

import discord
from discord import ActivityType, Status, VerificationLevel, VoiceRegion, utils
from discord.ext import commands

from src.colours import DISCORD_COLOURS

# Create a custom Bot class;
# Functions in this class can easily be used in cogs without imports;
# For example, my_function in this class can be called in a cog via self.bot.my_function()
class Procbot(commands.Bot):
    '''Custom `discord.ext.commands.Bot`-based class.'''

    # Gets the activity type of the specified member;
    # Called in a cog via self.bot.get_at(member)
    def get_at(self, member):
        # If the member has no activity, pass
        if member.activity is None:
            pass
        else:
            # If the activity type is unknown, return an empty string
            if member.activity.type == ActivityType.unknown:
                at = '\uFEFF'

            # Otherwise, return the specific activity type
            elif member.activity.type == ActivityType.playing:
                at = 'Playing'
            elif member.activity.type == ActivityType.streaming:
                at = 'Streaming'
            elif member.activity.type == ActivityType.listening:
                at = 'Listening'
            elif member.activity.type == ActivityType.watching:
                at = 'Watching'
            return at

    # Gets the status of the specified member;
    # Called in a cog via self.bot.get_status(member)
    def get_status(self, member):
        if member.status == Status.online:
            status = 'Online'
        elif member.status == Status.idle:
            status = 'Idle'
        elif member.status == Status.dnd:
            status = 'Do Not Disturb'
        elif member.status == Status.invisible:
            status = 'Offline'
        elif member.status == Status.offline:
            status = 'Offline'
        return status

    # Gets the verification level of the specified guild;
    # Called in a cog via self.bot.get_vl(guild)
    def get_vl(self, guild):
        if guild.verification_level == VerificationLevel.none:
            vl = 'None'
        elif guild.verification_level == VerificationLevel.low:
            vl = 'Low'
        elif guild.verification_level == VerificationLevel.medium:
            vl = 'Medium'
        elif guild.verification_level == VerificationLevel.high:
            vl = 'High'
        elif guild.verification_level == VerificationLevel.extreme:
            vl = '2FA Required'
        return vl

    # Gets the voice region of the specified guild;
    # Called in a cog via self.bot.get_vr(guild)
    def get_vr(self, guild):
        if guild.region == VoiceRegion.us_west:
            vr = 'US West'
        elif guild.region == VoiceRegion.us_east:
            vr = 'US East'
        elif guild.region == VoiceRegion.us_south:
            vr = 'US South'
        elif guild.region == VoiceRegion.us_central:
            vr = 'US Central'
        elif guild.region == VoiceRegion.eu_west:
            vr = 'EU West'
        elif guild.region == VoiceRegion.eu_central:
            vr = 'EU Central'
        elif guild.region == VoiceRegion.singapore:
            vr = 'Singapore'
        elif guild.region == VoiceRegion.london:
            vr = 'London'
        elif guild.region == VoiceRegion.sydney:
            vr = 'Sydney'
        elif guild.region == VoiceRegion.amsterdam:
            vr = 'Amsterdam'
        elif guild.region == VoiceRegion.frankfurt:
            vr = 'Frankfurt'
        elif guild.region == VoiceRegion.brazil:
            vr = 'Brazil'
        elif guild.region == VoiceRegion.hongkong:
            vr = 'Hong Kong'
        elif guild.region == VoiceRegion.russia:
            vr = 'Russia'
        elif guild.region == VoiceRegion.vip_us_east:
            vr = 'VIP US East'
        elif guild.region == VoiceRegion.vip_us_west:
            vr = 'VIP US West'
        elif guild.region == VoiceRegion.vip_amsterdam:
            vr = 'VIP Amsterdam'
        return vr

    # Updates experience data for the specified user;
    # Called in on_message
    async def update_data(self, user_xp, user):
        # If the user is a bot, pass
        if user.bot:
            pass

        # Otherwise, create an empty dict for the user;
        # Experience is set to 0 and level is set to 1;
        else:
            if not str(user.id) in user_xp:
                user_xp[str(user.id)] = {}
                user_xp[str(user.id)]['EXPERIENCE'] = 0
                user_xp[str(user.id)]['LEVEL'] = 1

    # Adds the specified amount of experience to the specified user;
    # Called in on_message
    async def add_experience(self, user_xp, user, xp):
        # If the user is a bot, pass
        if user.bot:
            pass

        # Otherwise, add the specified amount of experience to the specified user
        else:
            user_xp[str(user.id)]['EXPERIENCE'] += xp

    # Increase the specified user's level at a specific amount of experience;
    # Called in on_message to check if the user has levelled up or not;
    # If the user has levelled up, a message is sent to the channel saying so;
    async def level_up(self, user_xp, user, channel):
        # If the user is a bot, pass
        if user.bot:
            pass

        # Otherwise, check for a level up
        else:
            experience = user_xp[str(user.id)]['EXPERIENCE']
            level_start = user_xp[str(user.id)]['LEVEL']
            level_end = int(experience ** (1/4))

            # If the user has levelled up, send a message to the channel saying so
            if level_start < level_end:
                embed = discord.Embed()
                embed.title = 'Procbot'
                embed.description = f'**{user.name}** has levelled up!'
                embed.colour = 0x0000ff
                embed.add_field(name='Level', value=level_end, inline=True)
                embed.add_field(name='XP', value=experience, inline=True)
                embed.set_footer(text=datetime.datetime.now())
                await channel.send(embed=embed)
                user_xp[str(user.id)]['LEVEL'] = level_end

    # Set bot presence and log that the bot is ready
    async def on_ready(self):
        print('Beep boop. Boop beep?')
        print(f'Name: {str(self.user)}')
        print(f'ID: {self.user.id}')

        if len(self.guilds) == 1:
            await self.change_presence(activity=discord.Streaming(name='on 1 server! | .help', url='https://twitch.tv/kraken'))
        else:
            await self.change_presence(activity=discord.Streaming(name=f'on {len(self.guilds)} servers! | .help', url='https://twitch.tv/kraken'))

    # Reset bot presence and log that the bot's session has resumed;
    async def on_resumed(self):
        print('Procbot has reawakened.')
        print(f'Name: {str(self.user)}')
        print(f'ID: {self.user.id}')

        if len(self.guilds) == 1:
            await self.change_presence(activity=discord.Streaming(name='on 1 server! | .help', url='https://twitch.tv/kraken'))
        else:
            await self.change_presence(activity=discord.Streaming(name=f'on {len(self.guilds)} servers! | .help', url='https://twitch.tv/kraken'))

    # Do stuff whenever a message is sent;
    # This includes experience-related functions;
    # After everything has been called, process_commands is called;
    # If process_commands is not called, the bot won't respond to commands
    async def on_message(self, message):
        # If the message is from private messages, only process commands
        if not message.guild:
            await self.process_commands(message)

        # Otherwise, run experience, prefix and log-related functions
        else:
            # Open xp.json in read mode
            with open('xp.json', 'r') as fp:
                xp = json.load(fp)

            # Run experience-related functions
            await self.update_data(xp, message.author)
            await self.add_experience(xp, message.author, 5)
            await self.level_up(xp, message.author, message.channel)

            # If the bot's user ID isn't in xp.json, create an empty dict;
            # Experience is set to an extremely high number and level is set to 1
            if not str(self.user.id) in xp:
                xp[str(self.user.id)] = {}
                xp[str(self.user.id)]['LEVEL'] = 1
                xp[str(self.user.id)]['EXPERIENCE'] = int(2 ** 64)

            # Otherwise, add an insanely high amount of experience to the bot
            else:
                xp[str(self.user.id)]['LEVEL'] += 1
                xp[str(self.user.id)]['EXPERIENCE'] += int(2 ** 64)

            # Open xp.json in write mode
            with open('xp.json', 'w') as fp:
                # Write any file changes to xp.json
                json.dump(xp, fp, indent=4)

            # Open guilds.json in read mode
            with open('guilds.json', 'r') as fp:
                guilds = json.load(fp)

            # If the guild's ID isn't in guilds.json, create an empty dict;
            # Guild prefix is set to '.';
            # Default volume is set to 0.5
            if not str(message.guild.id) in guilds:
                guilds[str(message.guild.id)] = {}
                guilds[str(message.guild.id)]['GUILD_PREFIX'] = '.'
                guilds[str(message.guild.id)]['DEFAULT_VOLUME'] = 0.5

            # Open guilds.json in write mode
            with open('guilds.json', 'w') as fp:
                # Write any file changes to guilds.json
                json.dump(guilds, fp, indent=4)                

            # Open mod_logs.json in read mode
            with open('mod_logs.json', 'r') as fp:
                mod_logs = json.load(fp)

            # If the guild's ID isn't in mod_logs.json, create an empty dict;
            # Case counts are set to 0
            if not str(message.guild.id) in mod_logs:
                mod_logs[str(message.guild.id)] = {}
                mod_logs[str(message.guild.id)]['KICK_COUNT'] = 0
                mod_logs[str(message.guild.id)]['BAN_COUNT'] = 0
                mod_logs[str(message.guild.id)]['MUTE_COUNT'] = 0

            # Open mod_logs.json in write mode
            with open('mod_logs.json', 'w') as fp:
                # Write any file changes to mod_logs.json
                json.dump(mod_logs, fp, indent=4)

            # Process commands
            await self.process_commands(message)

    # Processes commands in edited messages
    async def on_message_edit(self, before, after):
        # Open guilds.json in read mode
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)

        # If the current guild is in guilds.json, fetch its prefix
        p = guilds[str(before.guild.id)]['GUILD_PREFIX']

        # If the original message was a command, pass
        if f'{p}help' or f'{p}kick' or f'{p}ban' or f'{p}mute' or f'{p}unmute' or f'{p}purge' or f'{p}setting' or f'{p}info' or f'{p}profile' or f'{p}serverinfo' or f'{p}load' or f'{p}unload' or f'{p}reload' or f'{p}logout' or f'{p}roll' or f'{p}gay' or f'{p}ping' or f'{p}cat' or f'{p}xp' or f'{p}play' or f'{p}pause' or f'{p}resume' or f'{p}skip' or f'{p}np' or f'{p}playlist' or f'{p}stop' or f'{p}volume' in before.content:
            # self.process_commands(before) re-invokes the recently invoked command, so use pass instead
            pass
        # If the original message wasn't a command, process the commands in the edited message
        else:
            await self.process_commands(after)

        # Open guilds.json in write mode
        with open('guilds.json', 'w') as fp:
            # Write any file changes to guilds.json
            json.dump(guilds, fp, indent=4)

    # Logs that a command has been invoked
    async def on_command(self, ctx):
        print(f'Invocation - Command \'{ctx.command}\' from {str(ctx.author)}')

    # Called whenever the bot has joined a guild;
    # Does things such as creating the 'Muted' role and updating the guild count
    async def on_guild_join(self, guild):
        # Update guild count
        if len(self.guilds) == 1:
            await self.change_presence(activity=discord.Streaming(name='on 1 server! | .help', url='https://twitch.tv/kraken'))
        else:
            await self.change_presence(activity=discord.Streaming(name=f'on {len(self.guilds)} servers! | .help', url='https://twitch.tv/kraken'))

        # Get a random role colour
        role_colour = random.choice(DISCORD_COLOURS)

        # Find the 'Muted' role
        role = utils.get(guild.roles, name='Muted')

        # If the 'Muted' role is non-existent, create it
        if role is None:
            role = await guild.create_role(name='Muted', reason='Role for mute command functionality.')

        # Find the 'Staff' role
        staff_role = utils.get(guild.roles, name='Staff')

        # If the 'Staff' role is non-existent, create it
        if staff_role is None:
            staff_role = await guild.create_role(name='Staff', colour=role_colour, hoist=True, reason='Role for server staff/moderators.')

        # Find the 'Admin' role
        admin_role = utils.get(guild.roles, name='Admin')

        # If the 'Admin' role is non-existent, create it
        if admin_role is None:
            admin_role = await guild.create_role(name='Admin', permissions=discord.Permissions(permissions=8), colour=role_colour, hoist=True, reason='Role for server moderators.')

        # Find all guild channels
        channels = utils.get(self.get_all_channels(), guild__name=guild.name)

        # Deny the 'Send Messages' permission to the 'Muted' role in all guild channels
        await channels.set_permissions(target=role, send_messages=False)

        # Open guilds.json in read mode
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)

        # If the guild's ID isn't in guilds.json, create an empty dict;
        # Guild prefix is set to '.';
        # Default volume is set to 0.5
        if not str(guild.id) in guilds:
            guilds[str(guild.id)] = {}
            guilds[str(guild.id)]['GUILD_PREFIX'] = '.'
            guilds[str(guild.id)]['DEFAULT_VOLUME'] = 0.5

        # Open guilds.json in write mode
        with open('guilds.json', 'w') as fp:
            # Write any file changes to guilds.json
            json.dump(guilds, fp, indent=4)

        # Open mod_logs.json in read mode
        with open('mod_logs.json', 'r') as fp:
            mod_logs = json.load(fp)

        # If the guild's ID isn't in guilds.json, create an empty dict;
        # Case counts are set to 0
        if not str(guild.id) in mod_logs:
            mod_logs[str(guild.id)] = {}
            mod_logs[str(guild.id)]['KICK_COUNT'] = 0
            mod_logs[str(guild.id)]['BAN_COUNT'] = 0
            mod_logs[str(guild.id)]['MUTE_COUNT'] = 0

        # Open mod_logs.json in write mode
        with open('mod_logs.json', 'w') as fp:
            # Write any file changes to mod_logs.json
            json.dump(mod_logs, fp, indent=4)

    # Called whenever the bot has been removed from a guild;
    # Updates the bot's visible guild count
    async def on_guild_remove(self, guild):
        # Update guild count
        if len(self.guilds) == 1:
            await self.change_presence(activity=discord.Streaming(name='on 1 server! | .help', url='https://twitch.tv/kraken'))
        else:
            await self.change_presence(activity=discord.Streaming(name=f'on {len(self.guilds)} servers! | .help', url='https://twitch.tv/kraken'))

    # Called whenever a member has joined a guild;
    # Finds a logs channel in the guild and logs that the member has joined
    async def on_member_join(self, member):
        # If the member's ID is the bot's user ID, pass
        if member.id == self.user.id:
            pass

        # Otherwise, log that the member has joined
        else:
            # Find the 'welcome' channel
            channel = utils.get(member.guild.text_channels, name='welcome')

            # Find the 'Staff' role
            staff_role = utils.get(member.guild.roles, name='Staff')

            # Get a random role colour
            role_colour = random.choice(DISCORD_COLOURS)

            # If the 'Staff' role is non-existent, create it
            if staff_role is None:
                staff_role = await member.guild.create_role(name='Staff', colour=role_colour, hoist=True, reason='Role for server staff/moderators.')

            # If the 'welcome' channel is non-existent, create it
            if channel is None:
                # Set channel overwrites for @everyone, the bot, and the 'Staff' role
                overwrites = {
                    member.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                    member.guild.me: discord.PermissionOverwrite(send_messages=True),
                    staff_role: discord.PermissionOverwrite(send_messages=True)
                }

                # Create the 'Information' category and the 'welcome' channel
                category = await member.guild.create_category_channel(name='Information', overwrites=overwrites, reason='Category for information-based channels.')
                channel = await member.guild.create_text_channel(name='welcome', overwrites=overwrites, category=category, reason='Channel for welcome and leave messages.')

            # Send the join message
            await channel.send(f'Welcome to the server, **{member.name}**! We\'re so happy to see you here! :tada:')

            # Open xp.json in read mode
            with open('xp.json', 'r') as fp:
                xp = json.load(fp)

            # Check xp.json
            await self.update_data(xp, member)

            # Open xp.json in write mode
            with open('xp.json', 'w') as fp:
                # Write any  file changes to xp.json
                json.dump(xp, fp, indent=4)

    # Called whenever a member has left a guild;
    # Finds a logs channel and logs that the member has left
    async def on_member_remove(self, member):
        # If the member's ID is the bot's user ID, pass
        if member.id == self.user.id:
            pass

        # Otherwise, log that the member has left
        else:
            # Find the 'welcome' channel
            channel = utils.get(member.guild.text_channels, name='welcome')

            # Find the 'Staff' role
            staff_role = utils.get(member.guild.roles, name='Staff')

            # Get a random role colour
            role_colour = random.choice(DISCORD_COLOURS)

            # If the 'Staff' role is non-existent, create it
            if staff_role is None:
                staff_role = await member.guild.create_role(name='Staff', colour=role_colour, hoist=True, reason='Role for server staff/moderators.')

            # If the channel is non-existent, create it
            if channel is None:
                # Set channel overwrites for @everyone, the bot, and the 'Staff' role
                overwrites = {
                    member.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                    member.guild.me: discord.PermissionOverwrite(send_messages=True),
                    staff_role: discord.PermissionOverwrite(send_messages=True)
                }

                # Create the 'Information' category and the 'welcome' channel
                category = await member.guild.create_category(name='Information', overwrites=overwrites, reason='Category for information-based channels.')
                channel = await member.guild.create_text_channel(name='welcome', overwrites=overwrites, category=category, reason='Channel for welcome and leave messages.')
            
            # Send the leave message
            await channel.send(f'We\'re sad to see you leave, **{member.name}**... :cry:')

    # Custom 'events';
    # on_kick, on_ban, on_mute;
    # Called in a cog via self.bot.on_kick(author, member, reason)
    async def on_kick(self, author, member, reason):
        # Open mod_logs.json in read mode
        with open('mod_logs.json', 'r') as fp:
            mod_logs = json.load(fp)

        # Find the 'mod-logs' channel
        channel = utils.get(member.guild.text_channels, name='mod-logs')

        # Find the 'Staff' role
        staff_role = utils.get(member.guild.roles, name='Staff')

        # Get a random role colour
        role_colour = random.choice(DISCORD_COLOURS)

        # If the 'Staff' role is non-existent, create it
        if staff_role is None:
            staff_role = await member.guild.create_role(name='Staff', colour=role_colour, hoist=True, reason='Role for server staff/moderators.')

        # If it doesn't exist, create it
        if channel is None:
            # Set channel overwrites for @everyone, the bot, and the 'Staff' role
            overwrites = {
                member.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                member.guild.me: discord.PermissionOverwrite(send_messages=True),
                staff_role: discord.PermissionOverwrite(send_messages=True)
            }

            # Create the 'Logs' category and the 'mod-logs' channel
            category = await member.guild.create_category(name='Logs', overwrites=overwrites, reason='Category for log-based channels.')
            channel = await member.guild.create_text_channel(name='mod-logs', overwrites=overwrites, category=category, reason='Channel for moderation logs.')

        # Fetch the number of kick cases
        case = mod_logs[str(member.guild.id)]['KICK_COUNT']

        # Send an embed to the 'mod-logs' channel
        embed = discord.Embed()
        embed.title = f':boot: Kick | Case {case}'
        embed.colour = 0x0000ff
        embed.add_field(name='Member Name', value=str(member), inline=False)
        embed.add_field(name='Member ID', value=str(member.id), inline=False)
        embed.add_field(name='Reason', value=str(reason), inline=False)
        embed.add_field(name='Kicked By', value=str(author), inline=False)
        embed.set_footer(text=datetime.datetime.now())
        await channel.send(embed=embed)

    # Called in a cog via self.bot.on_ban(author, member, reason)
    async def on_ban(self, author, member, reason):
        # Open mod_logs.json in read mode
        with open('mod_logs.json', 'r') as fp:
            mod_logs = json.load(fp)

        # Find the 'mod-logs' channel
        channel = utils.get(member.guild.text_channels, name='mod-logs')

        # Find the 'Staff' role
        staff_role = utils.get(member.guild.roles, name='Staff')

        # Get a random role colour
        role_colour = random.choice(DISCORD_COLOURS)

        # If the 'Staff' role is non-existent, create it
        if staff_role is None:
            staff_role = await member.guild.create_role(name='Staff', colour=role_colour, hoist=True, reason='Role for server staff/moderators.')

        # If it doesn't exist, create it
        if channel is None:
            # Set channel overwrites for @everyone, the bot, and the 'Staff' role
            overwrites = {
                member.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                member.guild.me: discord.PermissionOverwrite(send_messages=True),
                staff_role: discord.PermissionOverwrite(send_messages=True)
            }

            # Create the 'Logs' category and the 'mod-logs' channel
            category = await member.guild.create_category(name='Logs', overwrites=overwrites, reason='Category for log-based channels.')
            channel = await member.guild.create_text_channel(name='mod-logs', overwrites=overwrites, category=category, reason='Channel for moderation logs.')

        # Fetch the number of ban cases
        case = mod_logs[str(member.guild.id)]['BAN_COUNT']

        # Send an embed to the 'mod-logs' channel
        embed = discord.Embed()
        embed.title = f':no_entry_sign: Ban | Case {case}'
        embed.colour = 0x0000ff
        embed.add_field(name='Member Name', value=str(member), inline=False)
        embed.add_field(name='Member ID', value=str(member.id), inline=False)
        embed.add_field(name='Reason', value=str(reason), inline=False)
        embed.add_field(name='Banned By', value=str(author), inline=False)
        embed.set_footer(text=datetime.datetime.now())
        await channel.send(embed=embed)

    # Called in a cog via self.bot.on_mute(author, member, reason)
    async def on_mute(self, author, member, reason):
        # Open mod_logs.json in read mode
        with open('mod_logs.json', 'r') as fp:
            mod_logs = json.load(fp)

        # Find the 'mod-logs' channel
        channel = utils.get(member.guild.text_channels, name='mod-logs')

        # Find the 'Staff' role
        staff_role = utils.get(member.guild.roles, name='Staff')

        # Get a random role colour
        role_colour = random.choice(DISCORD_COLOURS)

        # If the 'Staff' role is non-existent, create it
        if staff_role is None:
            staff_role = await member.guild.create_role(name='Staff', colour=role_colour, hoist=True, reason='Role for server staff/moderators.')

        # If it doesn't exist, create it
        if channel is None:
            # Set channel overwrites for @everyone and the bot
            overwrites = {
                member.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                member.guild.me: discord.PermissionOverwrite(send_messages=True),
                staff_role: discord.PermissionOverwrite(send_messages=True)
            }

            # Create the 'Logs' category and the 'mod-logs' channel
            category = await member.guild.create_category(name='Logs', overwrites=overwrites, reason='Category for log-based channels.')
            channel = await member.guild.create_text_channel(name='mod-logs', overwrites=overwrites, category=category, reason='Channel for moderation logs.')

        # Fetch the number of mute cases
        case = mod_logs[str(member.guild.id)]['MUTE_COUNT']
        
        # Send an embed to the 'mod-logs' channel
        embed = discord.Embed()
        embed.title = f':zipper_mouth: Mute | Case {case}'
        embed.colour = 0x0000ff
        embed.add_field(name='Member Name', value=str(member), inline=False)
        embed.add_field(name='Member ID', value=str(member.id), inline=False)
        embed.add_field(name='Reason', value=str(reason), inline=False)
        embed.add_field(name='Muted By', value=str(author), inline=False)
        embed.set_footer(text=datetime.datetime.now())
        await channel.send(embed=embed)           

    # Global command error handler;
    # Called whenever an error is raised in a command;
    # If the cog or command has its own handler, the error handling is passed to it
    async def on_command_error(self, ctx, error):
        # Specify errors to be ignored
        ignored = (commands.CommandNotFound, commands.MissingRequiredArgument)

        # Fetch the original error
        error = getattr(error, 'original', error)

        # If the command has its own handler, return
        if hasattr(ctx.command, 'on_error'):
            return

        # If the cog has its own handler, return
        elif hasattr(ctx.cog, f'_{ctx.cog.__class__.__name__}__error'):
            return

        # If the error raised is in the ignored tuple, return
        elif isinstance(error, ignored):
            return

        # Otherwise, send the error message
        else:
            await ctx.send(f':x: Error: `{error}`')

    # Global event error handler;
    # Called whenever an error is raised in an event
    async def on_error(self, event, *args, **kwargs):
        print(f'Exception in event {event}:')
        print(traceback.format_exc())

    # Login
    def initialise(self):
        # Open settings.json in read mode
        with open('settings.json', 'r') as fp:
            settings = json.load(fp)

        # Fetch bot token
        token = settings['DISCORD_TOKEN']

        # Run bot
        self.run(token)

# Returns custom guild prefixes
def get_prefix(bot, message):
    # If the message is from private messages, return
    if not message.guild:
        return '.'

    # Otherwise, return the current guild's prefix
    else:
        # Open guilds.json in read mode
        with open('guilds.json', 'r') as fp:
            guilds = json.load(fp)

        # If the current guild isn't in guilds.json, create an empty dict;
        # Guild prefix is set to '.'
        if not str(message.guild.id) in guilds:
            guilds[str(message.guild.id)] = {}
            guilds[str(message.guild.id)]['GUILD_PREFIX'] = '.'

        # Open guilds.json in write mode
        with open('guilds.json', 'w') as fp:
            # Write any file changes to guilds.json
            json.dump(guilds, fp, indent=4)

        # Make '.' a prefix as well as the custom prefix for each guild
        prefixes = ['.', guilds[str(message.guild.id)]['GUILD_PREFIX']]

        # Return guild prefix
        return commands.when_mentioned_or(*prefixes)(bot, message)

print('discord.py {0.major}.{0.minor}.{0.micro} {0.releaselevel} | Procbot 1.0.0'.format(discord.version_info))
bot = Procbot(get_prefix)
bot.remove_command('help')
ext_dir = 'ext'

# Bot initialisation
if __name__ == '__main__':
    # Fetch cog files
    for ext in [f.replace('.py', '') for f in listdir(ext_dir) if isfile(join(ext_dir, f))]:
        try:
            # Load cog files
            bot.load_extension(ext_dir + '.' + ext)
        except (discord.ClientException, ModuleNotFoundError):
            # Print an error if needed
            print(f'ERROR: Failed to load {ext}')
            print(traceback.format_exc())
        else:
            # Log that the cog was successfully loaded
            print(f'Successfully loaded {ext}')
    # Run the bot         
    bot.initialise()
