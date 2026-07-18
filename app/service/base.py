from config import admins

class BaseService:
    def __init__(self, session, tg_id: int | None = None, purpose_tg_id: int | None = None, is_admin: bool = False):
        self.session = session
        self.tg_id = tg_id
        self.purpose_tg_id = purpose_tg_id or tg_id
        self.admins = admins
        self.is_admin = tg_id in self.admins and is_admin

