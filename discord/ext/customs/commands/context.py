import typing, discord
from .messageable import Member
from .command import Command


class Context(object):
    def __init__(self, message : discord.Message = None, author = typing.Optional[typing.Union[discord.User, Member, discord.Member]] = None, channel : typing.Union[discord.TextChannel, discord.VoiceChannel, discord.StageChannel] = None, guild : discord.Guild = None, bot = None):
        self.message = message
        self.channel = channel
        self.guild = guild
        self.author = author
        self.bot = bot

    @property
    def prefix(self):
        return self.bot.command_prefix
        
    async def send(self, content : str = None, *args, **kwargs):
        await self.channel.send(content, *args, **kwargs)
        
    async def reply(self, content : str = None, *args, **kwargs):
        await self.message.reply(content, *args, **kwargs)