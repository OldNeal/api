from app.logging.files import LogFiles, LogPaths

class LogsService:
    async def get_file_by_name(self, category: str, name: str):
        return LogFiles.get_by_name(category, name)

    async def get_files_by_mask(self, mask: str):
        return LogFiles.get_by_mask(mask)
        
    async def get_files_by_type(self, type: str):
        return LogFiles.get_by_type(type)

    async def get_all_files(self):
        return LogFiles.get_all()

    async def get_files(self, mask: str | None = None, type: str | None = None):
        if mask:
            return await self.get_files_by_mask(mask)
        elif type:
            return await self.get_files_by_type(type)
        else:
            return await self.get_all_files()
