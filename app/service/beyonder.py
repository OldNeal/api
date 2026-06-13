from app.logic.beyonder import BeyonderLogic
from app.service.base import BaseService

class BeyonderService(BaseService):
    def __init__(self, session, tg_id: int | None = None, purpose_tg_id: int | None = None):
        super().__init__(session, tg_id, purpose_tg_id)
        self.logic = BeyonderLogic(session, tg_id=tg_id, purpose_tg_id=purpose_tg_id, is_admin=self.is_admin)
        
    async def drink(self, path_name: str, seq: int = 9):
        return await self.logic.drink(path_name, seq)
    
    async def info(self):
        return await self.logic.info()

    async def upseq(self, add_seq: int = 1, path_name: str | None = None):
        return await self.logic.upseq(add_seq, path_name)
    
    async def downseq(self, remove_seq: int = 1, path_name: str | None = None):
        return await self.logic.downseq(remove_seq, path_name)
    
    async def replace_time(self, new_time):
        return await self.logic.replace_time(new_time)
 
    async def edit_time(self, delta, operator: str):
        return await self.logic.edit_time(delta, operator)

    async def kill(self):
        return await self.logic.kill()