


class CommandError(Exception):
    def __init__(self, message):
        super().__init__(message)

class CommandInvokeError(CommandError):
    def __init__(self, message):
        super().__init__(message)
        
class ArgumentNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)  