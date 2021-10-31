import discord
from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print("Start")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong")

bot.run("You token here")

