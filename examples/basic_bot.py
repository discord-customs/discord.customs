from discord.ext.customs.commands import Context, Bot
import discord
from discord.ext.customs.commands import DefaultHelp

bot = Bot(command_prefix="!", intents=discord.Intents.all())

@bot.command()
async def hello(ctx : Context):
    return await ctx.ui(help_cls=DefaultHelp)


bot.run("token")
