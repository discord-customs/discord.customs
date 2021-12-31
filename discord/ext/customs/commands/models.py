import asyncio


class Set:
    def __init__(self, args):
        self._set = set()
        self._dict = dict()

    def __repr__(self) -> str:
        return f"<Set set={self._set}>"

    def get(self, name):
        data = self._dict.get(name)
        if data is None:
            return data
        return data

    def set(self, name : str, value : str = None):
        try:
            self._dict[name] = value or name
            self._set.add(name or value)
            return self._dict[name]
        except Exception:
            raise Exception