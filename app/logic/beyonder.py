from app.logic.base import BaseLogic
from datetime import datetime, timedelta
from app.exception.beyonder import SeqDontExistException, UpseqNotComeException, ALreadyBeyonderException, PathDontEnterException, SeqBusyException, HaveActivityPointsError, MethodActionFullStudyError
from app.exception.wiki import PathDontSearchException
from app.validate.api.beyonder import (AnswerTimeReplace, 
                                       AnswerTimeRedact, 
                                       AnswerRedactSeq, 
                                       AnswerTimeInfo,
                                       Sequence,
                                       AnswerBeyonderList,
                                       AnswerBeyonderInfo,
                                       AnswerBody,
                                       AnswerPathInfo,
                                       AnswerStudyMethodAction,
                                       TimeRedact,
                                       Point,
                                       Points)
from app.logic.seq import sequences
from app.logic.activity import ACTIVITY_POINTS_TAG

class BeyonderLogic(BaseLogic):
    async def get_upseq_time(self, seq: int, ga_id: int, study_method_action: float = 0.0):
        paths = await self.dao.path.neighbor_paths(ga_id) if seq == 0 else None
        return self._get_upseq_time(seq, paths, study_method_action)

    def _get_upseq_time(self, seq: int, paths: int | None = None, study_method_action: float = 0.0):
        if 10 > seq > 0:
            upseq_time = timedelta(days=sequences.get(seq).days)
        elif seq == 0 and paths is not None:
            upseq_time = timedelta(days=sequences.get(seq).days*paths)
        else:
            raise SeqDontExistException(seq=seq)
        return datetime.now() + upseq_time*(1 - float(study_method_action)/2)


    def check_exist_seq(self, seq: int):
        if seq > 9 or seq < -1:
            raise SeqDontExistException(seq=seq)
        return seq

    async def info(self):
        user = await self.get_user()
        query_body = self.return_query_body(user)
        answer = AnswerBeyonderInfo(user=query_body, purpose=query_body).to_query(user)
        if user.beyonder is not None:
            activity_points = 0
            if user.inventory is not None:
                await user.inventory.awaitable_attrs.items
                item = user.inventory.items_by_sketch_tag.get(ACTIVITY_POINTS_TAG)
                if item is not None:
                    activity_points = item.quantity
            paths = (
                await self.dao.path.neighbor_paths(user.beyonder.seq.path.ga_id)
                if user.beyonder.seq_number == 0
                else None
            )
            answer.points = Points(
                study_method_action=user.beyonder.study_method_action(paths),
                study_points=Point(new=user.beyonder.study_points),
                activity_points=Point(new=activity_points),
                rsp=user.beyonder.rsp(paths),
            )
        return answer

    async def drink(self, path_name: str | None = None, path_id: int | None = None, seq: int = 9):
        if seq < 9:
            self.check_permission()
        self.check_exist_seq(seq)
        user = await self.get_user(self.purpose_user_id)
        if user.beyonder:
            raise ALreadyBeyonderException(path_name=user.beyonder.path_name, purpose_user=await self.query_body())
        if path_name == None and path_id == None:
            raise PathDontEnterException()
        if path_name:
            path = await self.dao.path.query_by_name(path_name)
        else:
            path = await self.dao.path.query_by_id(path_id)
        if path == None:
            raise PathDontSearchException(path_name=path_name, path_id=path_id)
        new_bndr = {
            'seq':path.sequences.get(seq), 
            'user_id':user.id, 
            'last_upseq':datetime.now(), 
            'next_upseq':await self.get_upseq_time(seq, path.ga_id)
            } 
        if seq == -1:
            new_bndr |= {
                'ga':path.ga,
                'seq':path.god, 
            }
        user.beyonder = await self.dao.beyonder.add(new_bndr)
        await self.dao.flush()
        self.botlog.drink(path.name, path.id, user.beyonder.seq.number, user.beyonder.seq.id)
        return AnswerRedactSeq(
            user=await self.query_body(self.user_id),
            purpose=await self.query_body(user.id),
            new=Sequence(seq=user.beyonder.seq_name, number=user.beyonder.seq_number, path=path.name, path_id=path.id, ga_id=path.ga_id),
            operation='add',
        )
  
    async def upseq(self, new_seq_number: int | None = None, path_name: str | None = None):
        user = await self.get_user(self.purpose_user_id, is_raise_not_beyonder=True)
        if user.beyonder.ga_id:
            raise SeqDontExistException('Вы уже ВД, дальше некуда')
        if new_seq_number is not None:
            new_seq_number = new_seq_number
            self.check_permission()
        else:
            new_seq_number = user.beyonder.seq_number - 1
        self.check_exist_seq(new_seq_number)
        await user.beyonder.awaitable_attrs.ga
        old_seq = user.beyonder.seq
        old_path = user.beyonder.seq.path
        remaining_time = user.beyonder.upseq_date
        if remaining_time is not None and remaining_time.total_seconds() > 0 and not self.is_admin:
            raise UpseqNotComeException(remaining_time=remaining_time)
        if path_name:
            path = await self.dao.path.query_by_name(path_name)
        else:
            path = user.beyonder.seq.path
        if path == None:
            raise PathDontSearchException(path_name=path_name)
        if new_seq_number == 0:
            if await self.dao.beyonder.query_by_path_id(path.id, new_seq_number):
                raise SeqBusyException(seq=new_seq_number, path_id=path.id)
        if new_seq_number == -1:
            if await self.dao.beyonder.query_ga_by_ga_id(path.ga_id):
                raise SeqBusyException(seq=new_seq_number, path_id=path.id)
        if new_seq_number < 0:
            user.beyonder.ga = path.ga
            new_seq = path.god
            user.beyonder.seq = new_seq
        else:
            new_seq = path.sequences.get(new_seq_number)
            user.beyonder.seq = new_seq
        user.beyonder.next_upseq = await self.get_upseq_time(new_seq_number, path.ga_id)
        user.beyonder.study_points = 0
        await self.dao.flush()
        self.botlog.upseq(old_path.name, old_path.id, old_seq.number, old_seq.id, path.name, path.id, user.beyonder.seq.number, user.beyonder.seq.id)
        return AnswerRedactSeq(
            user=await self.query_body(self.user_id),
            purpose=await self.query_body(user.id),
            new=Sequence(seq=user.beyonder.seq_name, number=user.beyonder.seq_number, path=path.name, path_id=path.id, ga_id=path.ga_id),
            old=Sequence(seq=old_seq.name, number=old_seq.number, path=old_path.name, path_id=old_path.id, ga_id=old_path.ga_id),
            operation='up',
        )
    
    async def downseq(self, new_seq_number: int | None = None, path_name: str | None = None):
        self.check_permission()
        user = await self.get_user(self.purpose_user_id, is_raise_not_beyonder=True)
        if new_seq_number == None:
            new_seq_number = user.beyonder.seq_number + 1
        self.check_exist_seq(new_seq_number)
        old_seq = user.beyonder.seq
        old_path = user.beyonder.seq.path
        if path_name:
            path = await self.dao.path.query_by_name(path_name)
        else:
            path = user.beyonder.seq.path
        if path == None:
            raise PathDontSearchException(path_name=path_name)
        if new_seq_number > 9:
            user.beyonder = None
        else:
            new_seq = path.sequences.get(new_seq_number)
            user.beyonder.seq = new_seq
            user.beyonder.ga = None
        user.beyonder.next_upseq = await self.get_upseq_time(user.beyonder.seq_number, path.ga_id)
        user.beyonder.study_points = 0
        await self.dao.flush()
        self.botlog.downseq(old_path.name, old_path.id, old_seq.number, old_seq.id, path.name, path.id, user.beyonder.seq.number, user.beyonder.seq.id)
        return AnswerRedactSeq(
            user=await self.query_body(self.user_id),
            purpose=await self.query_body(user.id),
            new=Sequence(seq=user.beyonder.seq_name, number=user.beyonder.seq_number, path=path.name, path_id=path.id, ga_id=path.ga_id) if user.beyonder else None,
            old=Sequence(seq=old_seq.name, number=old_seq.number, path=old_path.name, path_id=old_path.id, ga_id=old_path.ga_id),
            operation='down',
        )

    async def time_info(self, to_raise: bool = False):
        user = await self.get_user(is_raise_not_beyonder=True)
        remaining_time = user.beyonder.upseq_date
        if to_raise and remaining_time is not None and remaining_time.total_seconds() > 0:
            raise UpseqNotComeException(remaining_time=remaining_time)
        if user.beyonder.ga_id:
            raise SeqDontExistException('Вы уже ВД, дальше некуда')
        body = await self.query_body(user.id)
        return AnswerTimeInfo(
            user=body,
            purpose=body,
            next_upseq=user.beyonder.next_upseq,
            last_upseq=user.beyonder.last_upseq,
            total_seconds=remaining_time.total_seconds() if not remaining_time is None else None,
        ).to_query(user)
    
    async def replace_time(self, new_time: datetime):
        self.check_permission()
        user = await self.get_user(self.purpose_user_id, is_raise_not_beyonder=True)
        old_time = user.beyonder.next_upseq
        user.beyonder.next_upseq = new_time
        await self.dao.flush()
        self.botlog.time(old_time, new_time)
        return AnswerTimeReplace(
            user=await self.query_body(self.user_id),
            purpose=await self.query_body(user.id),
            old_time=old_time,
            new_time=user.beyonder.next_upseq,
        )
 
    async def edit_time(self, delta: timedelta, operator: str):
        self.check_permission()
        user = await self.get_user(self.purpose_user_id, is_raise_not_beyonder=True)
        old_time = user.beyonder.next_upseq
        match operator:
            case '-':
                user.beyonder.next_upseq -= delta
            case '+':
                user.beyonder.next_upseq += delta
        await self.dao.flush()
        self.botlog.time(old_time, user.beyonder.next_upseq)
        return AnswerTimeRedact(
            user=await self.query_body(self.user_id),
            purpose=await self.query_body(user.id),
            old_time=old_time,
            new_time=user.beyonder.next_upseq,
            seconds=delta.total_seconds(),
            operator=operator,
        )

    async def kill(self):
        if self.purpose_user_id and not self.purpose_user_id == self.user_id:
            self.check_permission()
        user = await self.get_user(self.purpose_user_id, is_raise_not_beyonder=True)
        old_beyonder = user.beyonder
        user.beyonder = None
        await self.dao.flush()
        self.botlog.kill(old_beyonder.path_name, old_beyonder.seq.path_id, old_beyonder.seq.number, old_beyonder.seq.id)
        return AnswerBody(
            user=await self.query_body(self.user_id),
            purpose=await self.query_body(user.id),
        )

    async def list(self, path_id: int, page: int | None = None, per_page: int = 5):
        beyonders, count = await self.dao.user.get_beyonders_by_path_id_paginated(
            path_id,
            page,
            per_page,
        )
        ga = await self.dao.user.get_ga_by_path_id(path_id)
        path = await self.dao.path.query_by_id(path_id)
        return AnswerBeyonderList(
            path=AnswerPathInfo(
                group=path.group, 
                name=path.name, 
                path_id=path.id, 
                emodzi=path.emodzi, 
                custom_emodzi_id=path.custom_emodzi_id
            ),
                ga=AnswerBeyonderInfo(user=self.return_query_body(ga), purpose=self.return_query_body(ga)).to_query(ga) if ga else None,
                beyonders=[AnswerBeyonderInfo(user=self.return_query_body(bndr), purpose=self.return_query_body(bndr)).to_query(bndr) for bndr in beyonders],
                page=self.pagination(page, per_page, count),
                count=count,
            )

    async def study_method_action(self, study_points: int):
        user = await self.get_user(self.user_id)
        await user.inventory.awaitable_attrs.items
        activity_points = user.inventory.items_by_sketch_tag.get(ACTIVITY_POINTS_TAG)
        if activity_points is None or activity_points.quantity - study_points < 0:
            raise HaveActivityPointsError()
        paths = await self.dao.path.neighbor_paths(user.beyonder.seq.path.ga_id) if user.beyonder.seq_number == 0 else None
        old_study_points = user.beyonder.study_points
        required_study_points = max(0, user.beyonder.rsp(paths) - old_study_points)
        if study_points > required_study_points:
            raise MethodActionFullStudyError(study_points=required_study_points)
        old_time = user.beyonder.next_upseq
        old_activity_points = activity_points.quantity
        old_precent_study = user.beyonder.precent_study_method_action(paths)
        activity_points.quantity -= study_points
        user.beyonder.study_points += study_points
        user.beyonder.next_upseq = self._get_upseq_time(
            user.beyonder.seq_number, 
            paths,
            user.beyonder.study_method_action(paths)
            )
        if activity_points.quantity <= 0:
            user.inventory.items.remove(activity_points)
        await self.dao.flush()
        self.botlog.study_method_action(
            user.beyonder.precent_study_method_action(paths) - old_precent_study,
            study_points,
            activity_points.quantity,
            activity_points.sketch.emodzi
            )
        return AnswerStudyMethodAction(
            user=await self.query_body(self.user_id),
            purpose=await self.query_body(user.id),
            points=Points(
                study_method_action=user.beyonder.study_method_action(paths) - old_precent_study / 100,
                study_points=Point(old=old_study_points, new=study_points),
                activity_points=Point(old=old_activity_points, new=activity_points.quantity),
                rsp=user.beyonder.rsp(paths)
            ),
            time=TimeRedact(
            old_time=old_time,
            new_time=user.beyonder.next_upseq,
            seconds=int((old_time - user.beyonder.next_upseq).total_seconds()),
            operator='-',
            )
        ).to_query(user)
