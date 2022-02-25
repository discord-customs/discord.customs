from discord.ext.customs import commands
import discord
import typing

from discord.ext.customs.commands.slash import SlashOption

class Simple(commands.Feature):
    def __init__(self, bot) -> None:
        super().__init__(bot)
        commands = [self.hello, self.bye]
        for cmd in commands:
            self.create_command(cmd)

    async def hello(self, ctx):
        return await ctx.send("hi")

    async def bye(self, ctx: commands.Context):
        return await ctx.reply(f"Bye, {ctx.author.name}")


bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.all(),
    application_id=844213992955707452, # replace with your application id
)
bot.integrate_feature(Simple(bot))



@bot.slash_command(options=[SlashOption(commands.SlashOptionType.string, "what", "what to say")])
async def hello(ctx: commands.SlashContext, what: commands.SlashOptionValue):
    await ctx.respond(commands.SlashResponse(content=what.value))

@bot.event
async def on_startup():
    print("Started")


bot.run("token")
