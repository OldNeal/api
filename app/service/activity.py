from app.logic.activity import ActivityLogic
from app.service.base import BaseService


class ActivityService(BaseService):
    def __init__(
        self,
        session,
        user_id: int | None = None,
        purpose_user_id: int | None = None,
        is_admin: bool = False,
    ):
        super().__init__(session, user_id, purpose_user_id, is_admin)
        self.logic = ActivityLogic(
            session,
            user_id=user_id,
            purpose_user_id=purpose_user_id,
            is_admin=self.is_admin,
        )

    async def get_activity_points(self, message_count: int = 1):
        return await self.logic.get_activity_points(message_count)

    async def reset_activity_points_limit(self, purpose_user_id: int):
        return await self.logic.reset_activity_points_limit(purpose_user_id)
