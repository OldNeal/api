from app.db.dao.models import DAO

class BaseLogic:
    def __init__(self, session, tg_id: int):
        self.dao = DAO(session)
        self.tg_id = tg_id

    async def get_user(self):
        return await self.dao.user.query_by_tg_id(self.tg_id)


    

