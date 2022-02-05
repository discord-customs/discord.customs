from discord.ext import commands
import discord

class Member(commands.Converter):
    async def convert(self, ctx, member_string : str):
        member = await commands.MemberConverter().convert(ctx, member_string)
        member = discord.Object(id=member.id)
        member = await ctx.bot.fetch_user(member.id)
        return member