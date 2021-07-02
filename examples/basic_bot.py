from discord.ext.customs import commands
import discord

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.command()
async def hello(ctx):
    await ctx.reply("Hello!")

bot.run("token")
