from sqlalchemy import text
from app.db.base import async_session_maker
from datetime import datetime
from app.logging.base import botlog
from app.exception.base import DBError

async def ping_db(logged: bool = False):
        async with async_session_maker() as session:
            try:
                start = datetime.now()
                response = await session.execute(text('SELECT 1'))
                if response:
                    end = datetime.now()
                    result = f'{int((end - start).total_seconds()*1000)}'
                    if logged:
                        botlog.logger.info('DB работает', ping=result)
                    return result
                raise DBError()
            except Exception as e:
                raise DBError(error=str(e))