from discord.ext.customs import commands
import discord

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

bot = commands.Bot(command_prefix="oahx ", intents=discord.Intents.all())
bot.integrate_feature(Simple(bot))

async def hello(ctx: commands.SlashContext):
    return await ctx.command.respond(ctx, commands.SlashResponse(content="Hi."))

@bot.event
async def on_ready():
    await bot.create_slash("hello", hello)

bot.run("token")
