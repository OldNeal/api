from pathlib import PurePath

class LogPaths:
    logs = PurePath('logs/')
    base = logs / PurePath('base/')
    beyonder = logs / PurePath('beyonder/')
    organ = logs / PurePath('organ/')
    newspaper = logs / PurePath('newspaper/')
    user = logs / PurePath('user/')
    question = logs / PurePath('question/')

    categories = {
        'base':base,
        'beyonder':beyonder,
        'organ':organ,
        'newspaper':newspaper,
        'user':user,
        'question':question,
    }

    @classmethod
    def get(cls, category: str):
        path = cls.categories.get(category)
        return path
    