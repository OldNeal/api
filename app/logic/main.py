from app.logic.base import BaseLogic
from app.validate.api.base import AnswerBaseInfo, QueryUserUpdate, AnswerBody
from app.db.models.main import TgUserDB, UserDB
from app.redis.links import links
from app.exception.base import ParametrValidationException, UserDontFind

class MainLogic(BaseLogic):
    links = links

    async def info(self):
        user =  await self.get_user()
        body = self.return_query_body(user)
        return AnswerBaseInfo(user=body, purpose=body).to_query(user)

    async def update(self, data: QueryUserUpdate):
        user = await self.dao.user.query_by_user_id(data.user_id)
        if user is None and data.telegram:
            user = await self.dao.user.query_by_tg_id(data.telegram.tg_id)
        if user is None:
            user = await self.dao.user.add({})
        if data.telegram:
            if user.tg_user:
                user.tg_user.username = data.telegram.username
                user.tg_user.fullname = data.telegram.fullname
            else:
                user.tg_user = TgUserDB(
                    tg_id=data.telegram.tg_id, 
                    username=data.telegram.username,
                    fullname=data.telegram.fullname
                )
                user.tg_id = data.telegram.tg_id
            await self.dao.flush()
        await links.cache_user(user.id, user.tg_id)
        return self.return_query_body(user)
    
    async def get_telegram(self, tg_id: int | None = None):
        if not tg_id is None:
            user = await self.dao.user.query_by_tg_id(tg_id)
        elif not self.purpose_user_id is None:
            user = await self.dao.user.query_by_user_id(self.purpose_user_id)
        else:
            raise ParametrValidationException('Вы не указали айди пользователя')
        if user is None:
            raise UserDontFind()
        await links.cache_user(user.id, user.tg_id)
        return self.return_query_body(user)