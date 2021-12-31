from discord import commands

class Member(commands.Converter):
    async def convert(self, ctx, member_string : str):
        member = await commands.MemberConverter().convert(ctx, member_string)
        return member