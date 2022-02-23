import asyncio
import typing
from functools import wraps


class Sequence:
    def __init__(self) -> None:
        self._store: typing.Dict[typing.Union[str, int], typing.Any] = {}
        self.index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index > len(self._store) - 1:
            raise StopAsyncIteration
        response = self._store[self.index]
        return response

    def append(
        self,
        value: typing.Any,
        key: typing.Optional[typing.Union[str, int]] = None,
    ):
        self._store[key or self.index] = value
        self.index += 1

    def add(self, *args, **kwargs):
        return self.append(*args, **kwargs)

    def remove(
        self,
        key: typing.Optional[typing.Union[str, int]] = None,
    ):
        return self._store.pop(key or self.index)


class Skipping:
    def __init__(self, message: str) -> None:
        self.msg = message

    def skip(self, msg: str):
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

    def set(self, name: str, value: str = None):
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
