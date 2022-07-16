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
import time
from datetime import datetime

import discord
from discord.ext import commands


class Settings:
    """
    open the settings.json file and load settings
    """
    with open(os.path.join(os.getcwd(), 'settings.json'), 'r', encoding='utf-8') as _token_file:
        _data = json.load(_token_file)
    channel_id = _data['channel_id']
    log_channel_id = _data['log_channel_id']
    server_id = _data['server_id']
    message = _data['message']
    roles = _data['roles']


client = commands.Bot(
    command_prefix=",",
    intents=discord.Intents.all()
)


# store all the reaction role emojis
ROLE_ICONS = []
for role in Settings.roles:
    ROLE_ICONS.append(role['reaction'])


def check(reaction, user):
    """
    check if the reaction is a valid emoji
    """
    return str(reaction.emoji) in ROLE_ICONS


@client.event
async def on_ready():
    """
    The on_reaction_add event is a little limited, 
    because it is only triggered by messages that are stored 
    in the Client.messages dequeue. 
    This is a cache (default size 5000) that stops your bot 
    from responding to activity on old messages. 
    There's no guarantee if you restart your bot that 
    it will still be "watching" that message.

    the thing you could do is send a message when your bot logs in, 
    and add the role to users who react to that message
    """

    # Notify that the bot is logged in
    print(f'Discord.py API version: {discord.__version__}')
    print(f'Python version: {platform.python_version()}')
    print(f'Logged in as {client.user} | {client.user.id}')
    global start_time
    start_time = time.time()

    # change the bot precense
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"teamsds.net"
        )
    )

    print("Bot is ready to be used!")

    # Get the channel, log channel and server
    channel = client.get_channel(Settings.channel_id)
    log_channel = client.get_channel(Settings.log_channel_id)
    guild = client.get_guild(Settings.server_id)
    if guild is None:  # if guild not in cache
        guild = await client.fetch_guild(Settings.server_id)

    # Send the text message to channel
    text = Settings.message
    message = await channel.send(text)
    await log_channel.send(f"`{datetime.now()}` - Sent the message to <#{Settings.channel_id}>")

    # Add all reactions specified in settings.json to the sent message
    for role in Settings.roles:
        await message.add_reaction(role['reaction'])
    await log_channel.send(f"`{datetime.now()}` - Added all reactions to the message")

    while True:
        # Wait for user reaction (asynchronously)
        reaction, user = await client.wait_for("reaction_add", check=check)

        for role in Settings.roles:  # loop through all roles in settings.json
            if str(reaction.emoji) == role['reaction']:

                # Get the role and user properly
                role_obj = discord.utils.get(guild.roles, name=role['name'])
                user = discord.utils.get(
                    guild.members,
                    name=f'{str(user).split("#")[0]}',
                    discriminator=f'{str(user).split("#")[-1]}'
                )

                # Add role to the user
                try:
                    await user.add_roles(role_obj)
                except Exception as e:
                    await log_channel.send(f"`{datetime.now()}` - Error adding {role['name']} role to <@{user.id}>: {e}")

                await log_channel.send(f"`{datetime.now()}` - Added {role['name']} role to <@{user.id}>")

if __name__ == "__main__":
    # open the token.txt, load the token, run the discord bot
    with open(os.path.join(os.getcwd(), 'token.txt'), 'r', encoding='utf-8') as _token_file:
        client.run(_token_file.read())
