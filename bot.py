import discord
import platform
import time
import os
import json
from discord.ext import commands


class Settings:
    with open(
        os.path.join(
            os.getcwd(),
            'settings.json'
        ),
        'r',
        encoding='utf-8'
    ) as _token_file:
        _data = json.load(_token_file)

    channel_id = _data['channel_id']
    message = _data['message']
    roles = _data['roles']


client = commands.Bot(command_prefix=",")


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

    # channel = client.get_channel(Settings.channel_id)


@client.command()
async def setup(ctx):
    text = Settings.message
    message = await ctx.send(text)
    for role in Settings.roles:
        await message.add_reaction(role['reaction'])


if __name__ == "__main__":
    with open(
        os.path.join(
            os.getcwd(),
            'token.txt'
        ),
        'r',
        encoding='utf-8'
    ) as _token_file:
        client.run(_token_file.read())
