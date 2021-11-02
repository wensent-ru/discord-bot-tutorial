from discord.ext import commands
import discord


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Module {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    async def info(self, ctx):
        region = ctx.guild.region
        owner = ctx.guild.owner.mention
        all = len(ctx.guild.members)
        members = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))
        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
        channels = [len(list(filter(lambda m: str(m.type) == "text", ctx.guild.channels))),
                    len(list(filter(lambda m: str(m.type) == "voice", ctx.guild.channels)))]
        embed = discord.Embed(title=f"{ctx.guild} information")
        embed.add_field(name="Statuses", value=f"Online: {statuses[0]} Idle: {statuses[1]} DND: {statuses[2]} Offline: {statuses[3]}")
        embed.add_field(name="Members", value=f"All: {all} Humans: {members} Bots: {bots}")
        embed.add_field(name="Channels", value=f"All: {channels[0] + channels[1]} Text: {channels[0]} Voice: {channels[1]}")
        embed.add_field(name="Members", value=f"All: {all} Humans: {members} Bots: {bots}")
        embed.add_field(name="Region", value=region)
        embed.add_field(name="Owner", value=owner)
        await ctx.send(embed=embed)

    @commands.command()
    async def user(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        roles = [role for role in member.roles]
        embed = discord.Embed(title=f"Info {member.name}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.display_name, inline=True)
        embed.add_field(name="Created at", value=member.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
        embed.add_field(name="Joined at", value=member.joined_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
        embed.add_field(name="Roles", value="".join(role.mention for role in roles), inline=True)
        embed.add_field(name="Top role", value=member.top_role.mention, inline=True)
        embed.add_field(name="Bot?", value=member.bot, inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))