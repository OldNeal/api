from app.db.base import async_session_maker

def get_session(commit: bool = True):
    async def wrapper():
        async with async_session_maker() as session:
            try:
                yield session
                if commit:
                    await session.commit()
            except Exception as e:
                await session.rollback()
                raise 
            finally:
                await session.close()
    return wrapper