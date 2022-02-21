import discord
from typing import *

class SelectOption(discord.SelectOption):
	def __init__(self, *, label: str, value: str = ..., description: Optional[str] = None, emoji: Optional[Union[str, discord.Emoji, discord.PartialEmoji]] = None, default: bool = False) -> None:
		super().__init__(label=label, value=value, description=description, emoji=emoji, default=default)
		self._label = label
		self._value = value
		self._description = description
		self._emoji = emoji
		self._default = default

	@classmethod
	def from_dict(cls, data) -> discord.SelectOption:
		return discord.SelectOption(**data)


class Select(discord.ui.Select):
	def __init__(self, ctx, options : List[SelectOption], callback : Coroutine):
		self.context = ctx
		self.callback_function = callback
		super().__init__(
            placeholder="Select Menu",
            min_values=1,
            custom_id="Dropdowns",
            max_values=1,
            options=options,
        )
		
	async def callback(self, interaction: discord.Interaction):
		return await self.callback_function(interaction=interaction, ctx=self.context)

class View(discord.ui.View):
	def __init__(self, *, items : List[Select], timeout: Optional[float] = 180):
		super().__init__(timeout=timeout)
		for item in items:
			self.add_item(item)