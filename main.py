import discord
from discord.ext import commands
import os
import json


def get_prefix(bot, message):
    with open("prefix.json", "r") as f:
        prefix = json.load(f)
    return prefix[str(message.guild.id)]


intents = discord.Intents().all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)


@bot.event
async def on_guild_join(guild):
    with open("prefix.json", "r") as f:
        prefix = json.load(f)
    prefix[str(guild.id)] = "."
    with open("prefix.json", "w") as f:
        json.dump(prefix, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open("prefix.json", "r") as f:
        prefix = json.load(f)
    prefix.pop(str(guild.id))
    with open("prefix.json", "w") as f:
        json.dump(prefix, f, indent=4)


@bot.command()
async def setprefix(ctx, new: str):
    with open("prefix.json", "r") as f:
        prefix = json.load(f)
    prefix[str(ctx.guild.id)] = new
    with open("prefix.json", "w") as f:
        json.dump(prefix, f, indent=4)
    await ctx.send(f"Новый префикс `{new}`")


@bot.command()
async def load(ctx, extension):
    extension = extension.lower()
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} loaded')


@bot.command()
async def unload(ctx, extension):
    extension = extension.lower()
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} unloaded')

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename.startswith("_"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run("You token here")
