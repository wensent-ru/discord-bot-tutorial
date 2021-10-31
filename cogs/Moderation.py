from discord.ext import commands
import discord


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Module {} is loaded'.format(self.__class__.__name__))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userid: int, reason='not specified'):
        user = await self.bot.fetch_user(userid)
        try:
            await ctx.guild.unban(user)
            await ctx.send(f"{user} has been unbanned. Reason: {reason}")
            return
        except:
            return await ctx.send(f"The user {user} is not banned!", delete_after=5)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.delete()
            await ctx.send("Not enough permissions to use this command", delete_after=5)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member = None, *, reason='not specified'):
        guild = ctx.guild
        await ctx.send(f"{ctx.author.display_name} banned a user {user.display_name}. Reason: {reason}")
        await guild.ban(user)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.delete()
            await ctx.send("Not enough permissions to use this command", delete_after=5)
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.message.delete()
            await ctx.send("Member not found", delete_after=5)
            return


def setup(bot):
    bot.add_cog(Moderation(bot))
