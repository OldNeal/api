from pathlib import PurePath

class LogPaths:
    logs = PurePath('logs/')
    base = logs / PurePath('base/')

    categories = {
        'base':base
    }

    @classmethod
    def get(cls, category: str):
        path = cls.categories.get(category)
        return path
    