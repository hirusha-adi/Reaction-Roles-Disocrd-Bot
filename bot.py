#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
MIT License

Copyright (c) 2022 Hirusha Adikari

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import os
import platform
from datetime import datetime

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='?')

with open("settings.json", 'r', encoding='utf-8') as _settings_data:
    settings = json.load(_settings_data)


@bot.event
async def on_ready():
    print(f'Discord.py API version: {discord.__version__}')
    print(f'Python version: {platform.python_version()}')
    print(f'Logged in as {bot.user} | {bot.user.id}')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{settings['presence']}"
        )
    )
    print("Bot is ready to be used!")


@bot.command(name="selfrole")
async def self_role(ctx):
    await ctx.channel.purge(limit=2)
    emojis = []
    roles = []
    for role in settings['roles']:
        roles.append(role['role'])
        emojis.append(role['emoji'])
    channel = bot.get_channel(int(settings['channel_id']))

    bot_msg = await channel.send(settings['message'])

    with open("reactions.json", "r") as f:
        self_roles = json.load(f)

    self_roles[str(bot_msg.id)] = {}
    self_roles[str(bot_msg.id)]["emojis"] = emojis
    self_roles[str(bot_msg.id)]["roles"] = roles

    with open("reactions.json", "w") as f:
        json.dump(self_roles, f)

    for emoji in emojis:
        await bot_msg.add_reaction(emoji)


@bot.event
async def on_raw_reaction_add(payload):
    msg_id = payload.message_id

    with open("reactions.json", "r") as f:
        self_roles = json.load(f)

    if payload.member.bot:
        return

    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)

        guild = bot.get_guild(payload.guild_id)
        log_channel = bot.get_channel(int(settings['log_channel_id']))

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                await payload.member.add_roles(role)
                await payload.member.send(f"Added **{selected_role}** Role!")
                await log_channel.send(f'`{datetime.now()}` - Added {selected_role} role to <@{payload.member.id}>')


@bot.event
async def on_raw_reaction_remove(payload):
    msg_id = payload.message_id

    with open("reactions.json", "r") as f:
        self_roles = json.load(f)

    if str(msg_id) in self_roles:
        emojis = []
        roles = []

        for emoji in self_roles[str(msg_id)]['emojis']:
            emojis.append(
                emoji)

        for role in self_roles[str(msg_id)]['roles']:
            roles.append(role)

        guild = bot.get_guild(payload.guild_id)
        log_channel = bot.get_channel(int(settings['log_channel_id']))

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]
                role = discord.utils.get(guild.roles, name=selected_role)
                member = await(guild.fetch_member(payload.user_id))
                if member is not None:
                    await member.remove_roles(role)
                    await payload.member.send(f"Removed **{selected_role}** Role!")
                    await log_channel.send(f'`{datetime.now()}` - Removed {selected_role} role from <@{payload.member.id}>')


if __name__ == "__main__":
    # open the token.txt, load the token, run the discord bot
    with open(os.path.join(os.getcwd(), 'token.txt'), 'r', encoding='utf-8') as _token_file:
        bot.run(_token_file.read())
