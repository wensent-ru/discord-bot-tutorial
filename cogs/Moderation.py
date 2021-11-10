from discord.ext import commands
import discord
from func import *
import datetime


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Module {} is loaded'.format(self.__class__.__name__))

    @tasks.loop()
    async def check_mutes(self):
        current = datetime.datetime.now()
        mutes = load_json("jsons/mutes.json")
        users, times = list(mutes.keys()), list(mutes.values())
        for i in range(len(times)):
            time = times[i]
            unmute = datetime.datetime.strptime(str(time), "%c")
            if unmute < current:
                user_id = users[times.index(time)]
                try:
                    member = await self.guild.fetch_member(int(user_id))
                    await member.remove_roles(self.mutedrole)
                    mutes.pop(str(member.id))
                except discord.NotFound:
                    pass
                write_json("jsons/mutes.json", mutes)

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
    async def mute(self, ctx, member: discord.Member = None, time: str = None, *, reason="не указана"):
        if member is None:
            return await ctx.send("User not specified")
        if member.bot is True:
            return await ctx.send("You can't mute the bot")
        if member == ctx.author:
            return await ctx.send("You can't mute yourself")
        if len(reason) > 150:
            return await ctx.send("The reason is too long")
        if member and member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send("You can't mute a man up with a role above yours")
        if time is None:
            return await ctx.send("You didn't specify the duration")
        else:
            try:
                seconds = int(time[:-1])
                duration = time[-1]
                if duration == "s":
                    pass
                if duration == "m":
                    seconds *= 60
                if duration == "h":
                    seconds *= 3600
                if duration == "d":
                    seconds *= 86400
            except:
                return await ctx.send("Wrong duration specified")
            mute_expiration = (datetime.datetime.now() + datetime.timedelta(seconds=int(seconds))).strftime("%c")
            role = self.mutedrole
            if not role:
                return await ctx.send("I can't find the mute role")
            mutes = load_json("jsons/mutes.json")
            try:
                member_mute = mutes[str(member.id)]
                return await ctx.send("The user is already in mute")
            except:
                mutes[str(member.id)] = str(mute_expiration)
                write_json("jsons/mutes.json", mutes)
                await member.add_roles(role)
                await member.move_to(channel=None)
                await ctx.send(f"{ctx.author.name} muted {member.display_name}"
                               f" until {mute_expiration} for a reason: {reason}")

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
        await member.remove_roles(self.mutedrole)
        await ctx.send(f"{ctx.author.name} unmute {member.display_name}")
        mutes = load_json("jsons/mutes.json")
        mutes.pop(str(member.id))
        write_json("jsons/mutes.json", mutes)

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

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = await self.bot.fetch_guild(...)  # You server id
        self.mutedrole = discord.utils.get(self.guild.roles, id=...)  # Mute role id
        self.check_mutes.start()


def setup(bot):
    bot.add_cog(Moderation(bot))
