from discord.ext.customs import commands
import discord
from discord.ext.customs.commands import DefaultHelp

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.command()
async def help(ctx : commands.Context):
    return await ctx.ui(help_cls=DefaultHelp)


bot.run("token")
