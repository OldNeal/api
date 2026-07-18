from app.logic.base import BaseLogic
from app.validate.api.base import AnswerBaseInfo

class MainLogic(BaseLogic):
    async def info(self):
        user =  await self.get_user()
        return AnswerBaseInfo(user=self.return_query_body(user)).to_query(user)
