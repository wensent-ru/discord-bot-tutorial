from discord.ext import commands
import discord
import random

# A list with links to reaction gifs (kiss, hug, punch and etc)
bite = ['https://media.discordapp.net/attachments/889573796070162432/889573892207804466/image0.gif',
        'https://media.discordapp.net/attachments/889573796070162432/889573892530782208/image1.gif',
        'https://media.discordapp.net/attachments/889573796070162432/889573893772283944/image3.gif',
        'https://media.discordapp.net/attachments/889573796070162432/889573894258843668/image4.gif',
        'https://media.discordapp.net/attachments/889573796070162432/889573894598574121/image5.gif',
        'https://media.discordapp.net/attachments/889573796070162432/889573895470972958/image7.gif',
        'https://media.discordapp.net/attachments/889573796070162432/889573896037224518/image8.gif'
        ]


class Reaction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Module {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    async def bite(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(color=member.color, title="Reaction: bite")
        embed.description = f"{ctx.author.mention} bites {member.mention}"
        url = (random.choice(bite))
        embed.set_image(url=url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Reaction(bot))
