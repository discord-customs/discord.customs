import discord, typing, re, inspect, importlib.util, sys, inspect, functools
from discord.ext import commands

__version__ = "1.0.3"

class CommandError(Exception):
    def __init__(self, message):
        super().__init__(self, message)

class CommandInvokeError(CommandError):
    def __init__(self, message):
        super().__init__(message)
        
class ArgumentNotFound(Exception):
    def __init__(self, message):
        super().__init__(self, message)        

class Context:
    def __init__(self, message : discord.Message = None, author = None, channel : typing.Union[discord.TextChannel, discord.VoiceChannel, discord.StageChannel] = None, guild : discord.Guild = None, bot : discord.Client = None):
        self.message = message
        self.channel = channel
        self.guild = guild
        self.author = author
        self.bot = bot
        self.prefix = bot.command_prefix
        
    async def send(self, content : str = None, *args, **kwargs):
        await self.channel.send(content, *args, **kwargs)
        
    async def reply(self, content : str = None, *args, **kwargs):
        await self.message.reply(content, *args, **kwargs)
                   
class Command:
    def __init__(self, name : str = None, callback : typing.Callable = None, description : str = None, args = None):
        self.name = name
        self.callback = callback
        self.description = description 
        self.args = args
                                                                
class Member(commands.Converter):
    async def convert(self, ctx, member_string : str):
        member = await commands.MemberConverter().convert(ctx, member_string)
        return member
        
class Bot(discord.Client):
    def __init__(self, command_prefix : str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_prefix = command_prefix
        self.commands = set()                       
 
    def get_command(self, name : str):
        for command in self.commands:
            if command.name == name:
                return command
            else:
                return None                                                                      
    async def on_message(self, message : discord.Message):
        await self.process_commands(message)     

    async def process_commands(self, message : discord.Message):
        context = await self.get_context(message)
        await self.invoke(ctx=context)   
       

    async def invoke(self, ctx):
        try:
            if ctx.message.content.startswith(self.command_prefix):
                message_content_without_prefix = ctx.message.content.strip(self.command_prefix)
                args_to_send = {}
                commands = self.commands
                command_names = {command.name for command in commands}
                for command_name in command_names:
                    command_content = message_content_without_prefix.split(" ")
                    if command_content[0] in command_names:
                        for cmd in commands:
                            if cmd.name == command_content[0]:
                                command = cmd                       
                    else:
                        raise CommandError(f"The command {command_content[0]} was not found.")              
                if not command.args:
                    raise ArgumentNotFound("You did not provide any arguments when you created the command.")
                message_content_without_cmd =  message_content_without_prefix.strip(command.name)
                if len(command.args) == 1:
                    if command.args[0] != "ctx":
                        raise ArgumentNotFound(f"You missed the ctx parameter in the command {command.name}.")  
                    else:
                        return await command.callback(ctx=ctx)
                else:
                    if command.args[0] != "ctx":
                        raise ArgumentNotFound(f"You missed the ctx parameter in the command {command.name}.")
                    else:                    
                        args = message_content_without_cmd.split(" ")
                        for arg in command.args:
                            for val in args:
                                args_to_send[arg] = val
                        args_to_send.pop("ctx")
                        return await command.callback(ctx=ctx, **args_to_send) 
        except Exception as e:
            raise CommandInvokeError(e) from e                                  
    def add_command(self, func : typing.Callable, name : str, description : str):
        if not isinstance(func, typing.Callable):
            raise CommandInvokeError(f'Failed to add command {name} because it is NOT a function and does not have the bot.command decorator.')
        params = inspect.signature(func).parameters
        param_names = []
        if not params:
            self.commands.add(Command(name=name, callback=func, description=description or None, args=None))
        else:
            for param in params:
                param_names.append(param)
            if param_names[0] == "ctx":
                return self.commands.add(Command(name=name, callback=func, description=description or None, args=param_names))                    
            else:
                raise ArgumentNotFound("You are missing the ctx parameter.") 
            return self.commands.add(Command(name=name, callback=func, description=description or None, args=param_names))
                                            
    def command(self, name : str = None, description : str = None):
        if self.command_prefix == None:
            raise RuntimeError("No command_prefix is set.")
            return                                   
        def command_wrapper(func : typing.Callable) -> typing.Callable:
            self.add_command(func, name = name or func.__name__, description = description)
        return command_wrapper
        
    async def get_context(self, message : discord.Message):
        return Context(message=message, author=message.author, channel=message.channel, guild=message.guild, bot=self) 
        
class ShardedBot(Bot, discord.AutoShardedClient):
    pass                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   