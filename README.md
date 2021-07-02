## discord.customs

Some customized-extensions you can add to your discord.py bot.

# Installation

```shell
python3 -m pip install discord.ext.customs
```

## Example

```python
import discord
from discord.ext.customs import commands

# Enable gateway intents on the developer portal

bot = commands.Bot(intents=discord.Intents.all())

@bot.command(name="some_command")
async def some_command(ctx):
    await ctx.send(f"Hello.")

bot.run("Token Here")
```

NOTE: Some of these extensions already exist in the library, so i've added more functionality to them.