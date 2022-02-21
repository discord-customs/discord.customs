import discord
from typing import *
from .command import Command
import typing


{
            "type": 4,
            "data": {
                "tts": False,
                "content": "Congrats on sending your command!",
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        }

class SlashResponse:
	def __init__(self, content: str = None, tts: bool = False, embeds: List[discord.Embed] = None, embed: discord.Embed = None, allowed_mentions: discord.AllowedMentions = None) -> None:
		self.content = content
		self.tts = tts
		self.embeds = embeds
		self.embed = embed
		self.allowed_mentions = allowed_mentions

	def to_dict(self):
		embeds = []
		data = {"tts": self.tts}
		if self.embeds:
			for embed in self.embeds:
				embeds.append(embed.to_dict())
			data["embeds"] = embeds
		if self.embeds and self.embed:
			raise RuntimeError("Cannot have `embeds` and `embed` set at the same time.")
		if self.embed:
			embeds.append(self.embed.to_dict())
			data["embeds"] = embeds
		if self.allowed_mentions:
			data["allowed_mentions"] = self.allowed_mentions.to_dict()
		if self.content:
			data["content"] = self.content
		return data

class SlashContext:
	def __init__(self, bot=None, interaction: discord.Interaction = None, command = None):
		self.channel = interaction.channel
		self.guild = interaction.guild
		self.author = interaction.user
		self.message = interaction.message
		self.bot = bot
		self.interaction = interaction
		self.command = command

class SlashCommand(Command):
	def __init__(self, name: str = None, callback: Coroutine = None, description: str = None, args=None, feature=None):
		super().__init__(name, callback, description, args, feature)
		self.responder: discord.webhook.async_.AsyncWebhookAdapter = discord.webhook.async_.async_context.get()
		self.data: dict = {"type": 4}

	async def __call__(self, ctx, *args, **kwargs):
		return await self.callback(ctx, *args, **kwargs)

	async def respond(self, ctx: SlashContext, response: SlashResponse):
		self.responded = True
		interaction: discord.Interaction = ctx.interaction
		self.data["data"] = response.to_dict()
		route = discord.http.Route("POST", f"/interactions/{interaction.id}/{interaction.token}/callback")
		await ctx.bot.http.request(route, headers={"Content-Type": "application/json"}, json=self.data)