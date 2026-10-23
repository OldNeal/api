from pathlib import PurePath

class LogPaths:
    logs = PurePath('logs/')
    base = logs / PurePath('base/')
    beyonder = logs / PurePath('beyonder/')
    organ = logs / PurePath('organ/')
    newspaper = logs / PurePath('newspaper/')

    categories = {
        'base':base,
        'beyonder':beyonder,
        'organ':organ,
        'newspaper':newspaper,
    }

    @classmethod
    def get(cls, category: str):
        path = cls.categories.get(category)
        return path
    