import asyncio


class Skipping():
    def __init__(self, message : str) -> None:
        self.msg = message

    def skip(self, msg : str):
        if self.msg.startswith(msg):
            try:
                msg = self.msg.split(msg)
                return msg[1]
            except Exception:
                return None
        else:
            return None

class Set:
    def __init__(self):
        self._set = set()
        self._dict = dict()

    def __repr__(self) -> str:
        return f"<Set set={self._set}>"

    def get(self, name):
        data = self._dict.get(name)
        return data

    def set(self, name : str, value : str = None):
        try:
            self._dict[name] = value
            self._set.add(value)
            return self._dict[name]
        except Exception:
            raise Exception

    def remove(self, name: str):
        del self._dict[name]
        thing = self.get(name)
        self._set.remove(thing)