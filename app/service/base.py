

class BaseService:
    def __init__(self, session, tg_id: int):
        self.session = session
        self.tg_id = tg_id

