import typing, discord
from .messageable import Member
from .command import Command
from .help_command import DefaultHelp


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
        author: typing.Union[discord.Member, Member, discord.User] = None,
        bot=None,
    ):

        self.message = message
        self.channel = channel
        self.guild = guild
        self.author = author
        self.bot = bot

    @property
    def prefix(self):
        return self.bot.command_prefix

    async def ui(self, send_help : bool = True, help_cls = None):
        if not send_help:
            ...
        if not help_cls:
            raise RuntimeError("Help class not specified")
        cls = help_cls(ctx=self)
        return await cls.send_bot_help()

    async def edit(self, message : discord.Message, content : str = None, *args, **kwargs):
        return await message.edit(content, *args, **kwargs)

    async def send(self, content: str = None, *args, **kwargs):
        return await self.channel.send(content, *args, **kwargs)

    async def reply(self, content: str = None, *args, **kwargs):
        return await self.message.reply(content, *args, **kwargs)
