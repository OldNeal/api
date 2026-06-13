from app.db.base import async_session_maker
from app.db.dao.models import DAO

async def check_user(tg_id: int, username: str | None, fullname: str | None):
        async with async_session_maker() as session:
            try:
                dao = DAO(session)
                user = await dao.user.query_by_tg_id(tg_id)
                if user:
                    user.tg_user.username = username
                    user.tg_user.fullname = fullname
                else: 
                    user = await dao.user.add({'tg_id':tg_id})
                    await dao.tguser.add({'tg_id':tg_id, 'username':username, 'fullname':fullname})
                await session.commit()
                return user
            except Exception as e:
                await session.rollback()
                raise 
            finally:
                await session.close()