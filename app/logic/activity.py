from app.logic.base import BaseLogic
from app.validate.api.base import (
    AnswerActivityPoints,
    AnswerActivityPointsAdd,
    AnswerActivityPointsDeduct,
    AnswerActivityPointsLimitReset,
)
from config import settings

ACTIVITY_POINTS_MESSAGE = 10

class ActivityLogic(BaseLogic):
    async def _admin_activity_answer(self, target, points: int = 0):
        admin = await self.get_user(self.user_id)
        return AnswerActivityPoints(
            user=self.return_query_body(admin),
            purpose=self.return_query_body(target),
            activity_points=target.activity_points,
            all_activity_points=target.all_activity_points,
            get_activity_points=points,
        )

    async def get_activity_points(self, message_count: int = 1):
        user = await self.get_user(self.user_id)
        activity_points = await self.store.activity.check_activity_points(
            self.user_id,
            message_count * ACTIVITY_POINTS_MESSAGE * settings.activity_points_factor,
        )
        user.activity_points += activity_points
        user.all_activity_points += activity_points
        await self.dao.flush()
        self.botlog.get_activity_points(activity_points, user.all_activity_points)
        return AnswerActivityPoints(
            user=self.return_query_body(user),
            purpose=self.return_query_body(user),
            activity_points=user.activity_points,
            all_activity_points=user.all_activity_points,
            get_activity_points=activity_points,
        )

    async def add_activity_points(self, purpose_user_id: int, points: int, reason: str | None = None):
        self.check_permission()
        user = await self.get_user(purpose_user_id)
        old_activity_points = user.activity_points
        user.activity_points += points
        await self.dao.flush()
        self.botlog.activity_points_add(self.user_id, purpose_user_id, points, reason)
        admin = await self.get_user(self.user_id)
        return AnswerActivityPointsAdd(
            user=self.return_query_body(admin),
            purpose=self.return_query_body(user),
            old_activity_points=old_activity_points,
            added_activity_points=points,
            activity_points=user.activity_points,
            all_activity_points=user.all_activity_points,
        )

    async def deduct_activity_points(self, purpose_user_id: int, points: int, reason: str | None = None):
        self.check_permission()
        user = await self.get_user(purpose_user_id)
        old_activity_points = user.activity_points
        user.activity_points -= points
        await self.dao.flush()
        self.botlog.activity_points_deduct(self.user_id, purpose_user_id, points, reason)
        admin = await self.get_user(self.user_id)
        return AnswerActivityPointsDeduct(
            user=self.return_query_body(admin),
            purpose=self.return_query_body(user),
            old_activity_points=old_activity_points,
            deducted_activity_points=points,
            activity_points=user.activity_points,
            all_activity_points=user.all_activity_points,
        )

    async def reset_activity_points(self, purpose_user_id: int, reason: str | None = None):
        self.check_permission()
        user = await self.get_user(purpose_user_id)
        removed_points = -user.activity_points
        user.activity_points = 0
        await self.dao.flush()
        self.botlog.activity_points_reset(self.user_id, purpose_user_id, removed_points, reason)
        return await self._admin_activity_answer(user, removed_points)

    async def reset_activity_points_limit(self, purpose_user_id: int):
        self.check_permission()
        user = await self.get_user(purpose_user_id)
        await self.store.activity.reset_activity_points_limit(purpose_user_id)
        admin = await self.get_user(self.user_id)
        return AnswerActivityPointsLimitReset(
            user=self.return_query_body(admin),
            purpose=self.return_query_body(user),
            activity_points=user.activity_points,
            all_activity_points=user.all_activity_points,
        )
