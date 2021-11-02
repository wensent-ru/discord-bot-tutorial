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

    @commands.command()
    # You must specify the roles ids that can use this command
    @commands.has_any_role()
    async def mute(self, ctx, member: discord.Member, *, reason='not specified'):
        await member.move_to(channel=None)
        # You must specify the name or role id of the mute role
        mute = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(mute)
        await ctx.send(f"{member.display_name} was muted by {ctx.author.name}. Reason: {reason}")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.message.delete()
            await ctx.send("Not enough permissions to use this command", delete_after=5)
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.message.delete()
            await ctx.send("Member not found", delete_after=5)
            return

    @commands.command()
    # You must specify the roles ids that can use this command
    @commands.has_any_role()
    async def unmute(self, ctx, member: discord.Member):
        # You must specify the name or role id of the mute role
        mute = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mute)
        await ctx.send(f"{member.display_name} was unmuted by {ctx.author.name}")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.message.delete()
            await ctx.send("Not enough permissions to use this command", delete_after=5)
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.message.delete()
            await ctx.send("Member not found", delete_after=5)
            return


def setup(bot):
    bot.add_cog(Moderation(bot))