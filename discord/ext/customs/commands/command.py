import typing

class Command:
    def __init__(self, name : str = None, callback : typing.Coroutine = None, description : str = None, args = None, feature = None):
        self.name = name
        self.callback = callback
        self.description = description 
        self.args = args
        self.feature = feature

    async def __call__(self, ctx, *args, **kwargs):
        return await self.callback(ctx, *args, **kwargs)