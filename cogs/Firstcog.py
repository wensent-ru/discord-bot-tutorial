from discord.ext import commands


class FirstCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Module {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog loaded")


def setup(bot):
    bot.add_cog(FirstCog(bot))