from app.logic.base import BaseLogic
from app.validate.api.base import AnswerBaseInfo, QueryUserUpdate, AnswerUsersBody
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

    async def search_users(
        self,
        user_id: int | None = None,
        tg_id: int | None = None,
        username: str | None = None,
        name: str | None = None,
    ):
        if (
            user_id is None
            and tg_id is None
            and not (username and username.strip().lstrip('@').strip())
            and not (name and name.strip())
        ):
            raise ParametrValidationException('Укажите хотя бы один параметр поиска')
        users = await self.dao.user.search_users(user_id, tg_id, username, name)
        return AnswerUsersBody(
            search_value=self.check_is_not_none(user_id, tg_id, username, name),
            users=[self.return_query_body(user) for user in users]
            )

    async def list_users(self):
        users = await self.dao.user.get_all_users()
        return AnswerUsersBody(users=[self.return_query_body(user) for user in users])


    async def delete_user(self, user_id: int):
        if user_id != self.user_id:
            self.check_permission()
        user = await self.dao.user.query_by_user_id(user_id)
        if user is None:
            raise UserDontFind()

        response = self.return_query_body(user)
        await self.dao.user.delete_one_by_id(user_id)
        await links.delete_user(user.id, user.tg_id)
        return response