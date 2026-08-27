from app.logic.organ import OrganLogic
from app.service.base import BaseService

class OrganService(BaseService):
    def __init__(self, session, tg_id: int | None = None, purpose_tg_id: int | None = None, organ_id: int | None = None, is_admin: bool = False):
        super().__init__(session, tg_id, purpose_tg_id, is_admin)
        self.logic = OrganLogic(session, tg_id=tg_id, purpose_tg_id=purpose_tg_id, organ_id=organ_id, is_admin=self.is_admin)

    async def member(self):
        return await self.logic.member()
    
    async def info(self):
        return await self.logic.info()

    async def members(self):
        return await self.logic.members()
    
    async def description(self):
        return await self.logic.description()
    
    async def search(self, name: str):
        return await self.logic.search(name)

    async def list(self):
        return await self.logic.list()
    
    async def organ_top_members(self):
        return await self.logic.organ_top_members()
    
    async def organ_top_days(self):
        return await self.logic.organ_top_days()
    
    async def login(self):
        return await self.logic.login()
    
    async def exit(self):
        return await self.logic.exit()

    async def create(self, name: str):
        return await self.logic.create(name)
    
    async def settings(self):
        return await self.logic.settings()
    
    async def settings_values(self):
        return await self.logic.settings_values()
    
    async def settings_redact(self, parametrs: dict):
        return await self.logic.settings_redact(parametrs)
    
    async def settings_default(self, default):
        return await self.logic.settings_default(default)
    
    async def uprank(self, rank: int | None = None):
        return await self.logic.rank_redact('up', rank)
    
    async def downrank(self, rank: int | None = None):
        return await self.logic.rank_redact('down', rank)
    
    async def kick(self):
        return await self.logic.kick()
    
    async def titul_redact(self, titul: str):
        return await self.logic.titul_redact(titul)
    
    async def titul_delete(self):
        return await self.logic.titul_redact()
    
    async def capture(self):
        return await self.logic.capture()
    
    async def give(self):
        return await self.logic.give()
