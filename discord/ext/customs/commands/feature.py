import discord, typing

"""
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
"""
class Feature():
	def __init__(self, bot) -> None:
		self.bot = bot

	async def add_command(self, func : typing.Awaitable, name : str = None):
		return self.bot.add_command(func, name or func.__name__, func.__doc__ or None)