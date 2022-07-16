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
import discord
import asyncio
import json
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print("Bot Is Now Online!")


@bot.command(name="selfrole")
async def self_role(ctx):

    emojis = answers[1].split(" ")
    roles = answers[2].split(" ")
    c_id = int(answers[3][2:-1])
    channel = bot.get_channel(c_id)

    bot_msg = await channel.send(answers[0])

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

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]

                role = discord.utils.get(guild.roles, name=selected_role)

                await payload.member.add_roles(role)
                await payload.member.send(f"You Got {selected_role} Role!")


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

        for i in range(len(emojis)):
            choosed_emoji = str(payload.emoji)
            if choosed_emoji == emojis[i]:
                selected_role = roles[i]
                role = discord.utils.get(guild.roles, name=selected_role)
                member = await(guild.fetch_member(payload.user_id))
                if member is not None:
                    await member.remove_roles(role)


if __name__ == "__main__":
    # open the token.txt, load the token, run the discord bot
    with open(os.path.join(os.getcwd(), 'token.txt'), 'r', encoding='utf-8') as _token_file:
        bot.run(_token_file.read())
