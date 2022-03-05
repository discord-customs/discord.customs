import discord
from discord.ext import commands
from typing import *

class Game:
	def __init__(self) -> None:
		pass

class Engine:
	def __init__(self, bot: commands.Bot, game: Game) -> None:
		self.bot = bot
		self.game = game