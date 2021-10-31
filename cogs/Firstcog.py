from discord.ext import commands
import discord


class FirstCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Module {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(title='title', description='description', color=ctx.author.color)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='text-1', value='value-1', inline=False)
        embed.add_field(name='text-2', value='value-2', inline=False)
        embed.add_field(name='text-3', value='value-3', inline=False)
        embed.add_field(name='text-1', value='value-1', inline=True)
        embed.add_field(name='text-2', value='value-2', inline=True)
        embed.add_field(name='text-3', value='value-3', inline=True)
        embed.set_image(url=ctx.author.avatar_url)
        embed.set_footer(text=f'Request from {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog loaded")


def setup(bot):
    bot.add_cog(FirstCog(bot))