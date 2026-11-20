from datetime import date

from app.redis.base import BaseHashs, BaseStore


class QuestionHashs(BaseHashs):
    DAILY_TAKEN_QUESTIONS = 'question:daily-taken:{user_id}:{day}'

    @classmethod
    def daily_taken_questions(cls, user_id: int, day: str):
        return cls.DAILY_TAKEN_QUESTIONS.format(user_id=user_id, day=day)


class QuestionStore(BaseStore):
    hashs_cls = QuestionHashs
    hashs: type[QuestionHashs]
    DAILY_TAKEN_QUESTIONS_TTL = 172800
    TAKE_QUESTION_SCRIPT = """
        local count = tonumber(redis.call('GET', KEYS[1]) or '0')
        if count >= tonumber(ARGV[1]) then
            return 0
        end
        count = redis.call('INCR', KEYS[1])
        if count == 1 then
            redis.call('EXPIRE', KEYS[1], tonumber(ARGV[2]))
        end
        return count
    """

    def daily_taken_questions_key(self, user_id: int):
        return self.hashs.daily_taken_questions(user_id, date.today().isoformat())

    async def get_daily_taken_questions(self, user_id: int):
        count = await self.client.get(self.daily_taken_questions_key(user_id))
        return int(count) if count else 0

    async def get_daily_taken_questions_limit(self, user_id: int):
        key = self.daily_taken_questions_key(user_id)
        count = await self.client.get(key)
        ttl = await self.client.pttl(key)
        return int(count) if count else 0, max(0, ttl // 1000) if ttl >= 0 else 0

    async def take_question(self, user_id: int, daily_limit: int):
        count = await self.client.eval(
            self.TAKE_QUESTION_SCRIPT,
            1,
            self.daily_taken_questions_key(user_id),
            daily_limit,
            self.DAILY_TAKEN_QUESTIONS_TTL,
        )
        return int(count) > 0
