import discord, typing, re, inspect, importlib.util, sys, inspect
from discord.ext import commands

__version__ = "1.0.2"

class ExtensionError(Exception):
    def __init__(self, message):
        super().__init__(self, message)
        
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
        
class Extension:
    def __init__(self, bot):
        self.bot = bot
        self.commands = {}
        self.command_list = [method for method in dir(self) if method.startswith('__') is False]
        if not self.command_list:
            raise ExtensionError("Extension {self.__class__.__name__} does not have any commands.")
        else:
            for command in self.command_list:
                _command = getattr(self, command, None)
                params = inspect.signature(_command).parameters
                param_names = []
                if not params:
                    bot.commands[_command.__name__] = Command(name=_command.__name__, callback=_command, description=_command.__doc__ or None, args=None) 
                    self.commands[_command.__name__] = Command(name=_command.__name__, callback=_command, description=_command.__doc__ or None, args=None) 
                else:
                    for param in params:
                        param_names.append(param)    
                    self.commands[_command.__name__] = Command(name=_command.__name__, callback=_command, description=_command.__doc__ or None, args=param_names)
                    bot.commands[_command.__name__] = Command(name=_command.__name__, callback=_command, description=_command.__doc__ or None, args=param_names)                                                                                        
class Member(commands.Converter):
    async def convert(self, ctx, member_string : str):
        member = await commands.MemberConverter().convert(ctx, member_string)
        return member
              
class Bot(discord.Client):
    def __init__(self, command_prefix : str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_prefix = command_prefix
        self.commands = {}
        self.extensions = {}
        
    def add_extension(self, class_module):
        class_module(self)               

    def _load_from_module_spec(self, spec, key):
        lib = importlib.util.module_from_spec(spec)
        sys.modules[key] = lib
        try:
            spec.loader.exec_module(lib)
        except Exception as e:
            del sys.modules[key]
            raise ExtensionError(key, e) from e

        try:
            setup = getattr(lib, 'setup')
        except AttributeError:
            del sys.modules[key]
            raise ExtensionError("Extension does not have \"setup\" function.")

        try:
            setup(self)
        except Exception as e:
            del sys.modules[key]
            self._remove_module_references(lib.__name__)
            self._call_module_finalizers(lib, key)
            raise errors.ExtensionFailed(key, e) from e
        else:
            self.extensions[key] = lib

    def _resolve_name(self, name, package):
        try:
            return importlib.util.resolve_name(name, package)
        except ImportError:
            raise ExtensionError(f"{name} was not found.")

    def load_extension(self, name, *, package=None):
        name = self._resolve_name(name, package)
        if name in self.extensions:
            raise ExtensionError(f"{name} is already loaded.")

        spec = importlib.util.find_spec(name)
        if spec is None:
            raise ExtensionError(f"{name} was not found.")

        self._load_from_module_spec(spec, name)
        
                        
    async def on_message(self, message : discord.Message):
        await self.process_commands(message)     

    async def process_commands(self, message : discord.Message):
        context = await self.get_context(message)
        await self.invoke(ctx=context)   
                           
    async def invoke(self, ctx):
        if ctx.message.content.startswith(self.command_prefix):
            message_content = ctx.message.content.strip(self.command_prefix)
            sent_args = {}
            for name in self.commands:
                command = self.commands[name]
                if not command.args:
                    if message_content == name:
                        return await command.callback(ctx=ctx)
                else:
                    content = message_content.strip(name)
                    content = content.split(' ')                   
                                      
                    if not content:
                        raise ArgumentNotFound(f"You have missed one of these arguments: {', '.join(command.args)}")
                    else:                   
                        for arg in command.args:
                            for value in content:
                                if value.startswith("<@"):
                                    value = await Member().convert(ctx, value)
                                sent_args[arg] = value
                    sent_args.pop("ctx")
                    try:
                        sent_args.pop("self")
                    except KeyError:
                        return await command.callback(ctx=ctx, **sent_args)
                    return await command.callback(ctx=ctx, **sent_args)
                    
            
        
    def command(self, name : str = None, description : str = None):
        if self.command_prefix == None:
            raise RuntimeError("No command_prefix is set.")
            return
        def command_wrapper(func : typing.Callable) -> typing.Callable:
            params = inspect.signature(func).parameters
            param_names = []
            if not params:
                self.commands[name or func.__name__] = Command(name=name or func.__name__, callback=func, description=description or None, args=None) 
            else:
                for param in params:
                    param_names.append(param)    
                self.commands[name or func.__name__] = Command(name=name or func.__name__, callback=func, description=description or None, args=param_names) 
        return command_wrapper
        
    async def get_context(self, message : discord.Message):
        return Context(message=message, author=message.author, channel=message.channel, guild=message.guild, bot=self) 
        
class ShardedBot(Bot, discord.AutoShardedClient):
    pass                                                                                                                                                                                                                                                                             