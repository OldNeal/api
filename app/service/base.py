from config import admins

class BaseService:
    def __init__(self, session, user_id: int | None = None, purpose_user_id: int | None = None, is_admin: bool = False):
        self.session = session
        self.user_id = user_id
        self.purpose_user_id = purpose_user_id or user_id
        self.admins = admins
        self.is_admin = user_id in self.admins and is_admin

