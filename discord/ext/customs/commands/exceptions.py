import typing, sys
import aioconsole, asyncio
class Error:
    """
    Common base class for all exceptions.
    """
    def __init__(self, message : typing.AnyStr, status_code : int, traceback : str) -> None:
        self.err = f"{traceback}: (status code: {status_code}) {message}"
        self.st = status_code
        
    async def print_error(self):
        print(self.err, file=sys.stderr)

class CommandError(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CommandInvokeError(CommandError):
    pass
        
class ArgumentNotFound(Error):
    pass

class MissingParameter(CommandInvokeError):
    pass

async def raise_error(exception : Error):
    return await exception.print_error()