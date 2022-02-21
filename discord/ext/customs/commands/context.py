import typing, discord
from .command import Command
from .option import Select, SelectOption, View
from .help_command import DefaultHelp
from .slash import *


class Context(object):
    def __init__(
        self,
        message: discord.Message = None,
        channel: typing.Union[
            discord.TextChannel,
            discord.StageChannel,
            discord.VoiceChannel,
            discord.GroupChannel,
        ] = None,
        guild: discord.Guild = None,
        author: typing.Union[discord.Member, discord.User] = None,
        bot=None,
        interaction: discord.Interaction = None,
        command: typing.Union[SlashCommand, Command] = None,
    ):

        self.message = message
        self.channel = channel
        self.guild = guild
        self.author = author
        self.bot = bot
        self._interaction = interaction
        self.command = command

    @property
    def interaction(self):
        return self._interaction

    @property
    def prefix(self):
        if self.interaction:
            return "/"
        return self.bot.command_prefix

    async def ui(
        self,
        base: typing.Union[str, discord.Embed],
        context: Select = None,
        send_help: bool = True,
        help_cls=None,
    ):
        if not send_help:
            if not context:
                raise RuntimeError("Select context not specified")
            return (
                await self.send(base, view=View(items=[context]), reply=True)
                if isinstance(base, str)
                else await self.send(embed=base, view=View(items=[context]), reply=True)
            )
        if not help_cls:
            raise RuntimeError("Help class not specified")
        cls = help_cls(ctx=self)
        return await cls.send_bot_help()

    async def edit(
        self, message: discord.Message, content: str = None, *args, **kwargs
    ):
        return await message.edit(content, *args, **kwargs)

    async def send(self, content: str = None, reply: bool = False, *args, **kwargs):
        return (
            await self.channel.send(content, *args, **kwargs)
            if not reply
            else await self.reply(content, *args, **kwargs)
        )

    async def reply(self, content: str = None, *args, **kwargs):
        return await self.message.reply(content, *args, **kwargs)
