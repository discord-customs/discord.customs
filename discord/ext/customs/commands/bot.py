from sre_constants import JUMP
from .exceptions import *
import typing, discord, re
from .command import Command
from .context import Context
from .params import Parameter
import inspect, discord
from .models import Set

cset = Set

class Bot(discord.Client):
    def __init__(self, command_prefix : str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_prefix = command_prefix
        self.commands = cset()         
 
    def get_command(self, name : str):
        data = self.commands.get(name)
        if not data:
            return None
        return data

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
            raise CommandInvokeError(f'Failed to add command {name}: Not Function')
        params = inspect.signature(func).parameters
        param_names = set()
        if not params:
            self.commands.set(name, value=Command(name=name, callback=func, description=description or None, args=None))
        else:
            for param in params:
                param_names.add(Parameter(name=param))
            iterator = iter(param_names)
            first_param = next(iterator, None)
            if first_param == "ctx":
                return self.commands.set(name=name, value=Command(name=name, callback=func, description=description or None, args=param_names))                    
            else:
                raise ArgumentNotFound("You are missing the ctx parameter.") 
            return self.commands.set(name, value=Command(name=name, callback=func, description=description or None, args=param_names))
                                            
    def command(self, name : str = None, description : str = None):
        if self.command_prefix is None:
            raise RuntimeError("No command_prefix set.")                                  
        def command_wrapper(func : typing.Callable) -> typing.Callable:
            self.add_command(func, name = name or func.__name__, description = description)
        return command_wrapper
        
    async def get_context(self, message : discord.Message):
        try:
            return Context(message=message, author=message.author, channel=message.channel, guild=message.guild, bot=self) 
        except Exception:
            raise Exception("A parameter is not provided in the message.")

class ShardedBot(Bot, discord.AutoShardedClient):
    pass  