import discord
import platform
import time
import os
import json
from discord.ext import commands
from datetime import datetime


class Settings:
    with open(os.path.join(os.getcwd(), 'settings.json'), 'r', encoding='utf-8') as _token_file:
        _data = json.load(_token_file)
    channel_id = _data['channel_id']
    log_channel_id = _data['log_channel_id']
    server_id = _data['server_id']
    message = _data['message']
    roles = _data['roles']


client = commands.Bot(command_prefix=",", intents=discord.Intents.all())


ROLE_ICONS = []
for role in Settings.roles:
    ROLE_ICONS.append(role['reaction'])


def check(reaction, user):
    return str(reaction.emoji) in ROLE_ICONS


@client.event
async def on_ready():
    print(f'Discord.py API version: {discord.__version__}')
    print(f'Python version: {platform.python_version()}')
    print(f'Logged in as {client.user} | {client.user.id}')
    global start_time
    start_time = time.time()
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"teamsds.net"
        )
    )
    print("Bot is ready to be used!")
    channel = client.get_channel(Settings.channel_id)
    log_channel = client.get_channel(Settings.log_channel_id)
    guild = client.get_guild(Settings.server_id)
    if guild is None:
        # if guild not in cache
        guild = await client.fetch_guild(Settings.server_id)
    text = Settings.message
    message = await channel.send(text)
    await log_channel.send(f"`{datetime.now()}` - Sent the message to <#{Settings.channel_id}>")
    for role in Settings.roles:
        await message.add_reaction(role['reaction'])
    await log_channel.send(f"`{datetime.now()}` - Added all reactions to the message")
    while True:
        reaction, user = await client.wait_for("reaction_add", check=check)
        for role in Settings.roles:
            if str(reaction.emoji) == role['reaction']:
                role_obj = discord.utils.get(guild.roles, name=role['name'])
                user = discord.utils.get(
                    guild.members,
                    name=f'{str(user).split("#")[0]}',
                    discriminator=f'{str(user).split("#")[-1]}'
                )
                try:
                    await user.add_roles(role_obj)
                except Exception as e:
                    await log_channel.send(f"`{datetime.now()}` - Error adding {role['name']} role to <@{user.id}>: {e}")
                await log_channel.send(f"`{datetime.now()}` - Added {role['name']} role to <@{user.id}>")

if __name__ == "__main__":
    with open(os.path.join(os.getcwd(), 'token.txt'), 'r', encoding='utf-8') as _token_file:
        client.run(_token_file.read())
