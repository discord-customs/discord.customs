from discord.ext.commands.errors import CommandNotFound
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
        await self.invoke(context) 

    async def invoke(self, ctx: Context):
        try:
            regex = re.compile(f'^{self.command_prefix}')
            ## regex=re.compile('^hello|^john|^world')
            if re.match(regex, ctx.message.content):
                content = re.sub(self.command_prefix, "", ctx.message.content)
                ctx.message.content = content
                found_command = [cmd for cmd in self.commands._set if ctx.message.content.startswith(cmd)]
                if not found_command:
                    raise CommandNotFound(f"Command \"{content}\" not found")
                found_command = found_command[0]
                command = self.commands.get(found_command)
                command_parameters = [param for param in (inspect.signature(command.callback))._parameters.keys()]
                needed_parameters = command_parameters
                if "ctx" not in command_parameters:
                    return await raise_error(MissingParameter("Missing \"ctx\" parameter", status_code=1, traceback="Missing Parameter"))
                parameters = {"ctx": ctx}
                return await command.callback(**parameters)
                #content = re.sub(found_command, "", ctx.message.content)
                
                

                

        except Exception as e:
            return await raise_error(CommandError(f"{e}", status_code=1, traceback="Error"))

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
            passed_ctx = False
            command = Command(name=name, callback=func, description=description or None, args=param_names)                    
            cmd = self.commands.get(name)
            return self.commands.set(name=name, value=Command(name=name, callback=func, description=description or None, args=param_names))  
                                            
    def command(self, name : str = None, description : str = None):
        if self.command_prefix is None:
            raise RuntimeError("No command_prefix set.")                                  
        def command_wrapper(func : typing.Callable) -> typing.Callable:
            self.add_command(func, name = name or func.__name__, description = description)
        return command_wrapper
        
    async def get_context(self, message : discord.Message):
        try:
            context = Context(message=message, author=message.author, channel=message.channel, guild=message.guild, bot=self) 
            if message.author.id == self.user.id:
                return context
            return context
        except Exception:
            return await raise_error(MissingParameter("A parameter is missing", status_code=1, traceback="Missing Parameter"))

class AutoShardedBot(Bot, discord.AutoShardedClient):
    pass  