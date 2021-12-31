import typing

class Command:
    def __init__(self, name : str = None, callback : typing.Callable = None, description : str = None, args = None):
        self.name = name
        self.callback = callback
        self.description = description 
        self.args = args