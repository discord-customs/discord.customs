import discord, typing
from .command import Command
from .models import Set


class FeatureBase:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.commands = Set()
        self.name = self.__class__.__name__

    def create_command(self, callback: typing.Awaitable):
        self.bot.add_command(
            name=callback.__name__,
            description=callback.__doc__,
            feature=self,
            func=callback,
        )


class Feature(FeatureBase):
    pass
