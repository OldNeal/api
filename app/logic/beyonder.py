from app.logic.base import BaseLogic
from datetime import datetime, timedelta
from app.exception.beyonder import SeqDontExistException, UpseqNotComeException, ALreadyBeyonderException, PathDontEnterException
from app.exception.wiki import PathDontSearchException
from app.validate.api.beyonder import (AnswerTimeReplace, 
                                       AnswerTimeRedact, 
                                       AnswerRedactSeq, 
                                       AnswerTimeInfo,
                                       Sequence)
upseq_time = {
  9:'',
  8:7,
  7:14,
  6:21,
  5:30,
  4:60,
  3:90,
  2:120,
  1:150,
  0:180,  
  -1:180,
}

class BeyonderLogic(BaseLogic):
    def get_upseq_time(sef, seq: int):
        return datetime.now()+timedelta(days=upseq_time.get(seq-1)) if seq > -1 else None

    def check_exist_seq(self, seq: int):
        if seq > 9 or seq < -1:
            raise SeqDontExistException(seq=seq)
        return seq

    async def drink(self, path_name: str | None = None, path_id: int | None = None, seq: int = 9):
        if seq < 9:
            self.check_permission()
        self.check_exist_seq(seq)
        user = await self.get_user(self.purpose_tg_id)
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
            'next_upseq':self.get_upseq_time(seq)
            } 
        if seq == -1:
            new_bndr |= {
                'ga':path.ga,
                'seq':path.sequences.get(0), 
            }
        user.beyonder = await self.dao.beyonder.add(new_bndr)
        await self.dao.flush()
        self.botlog.drink(path.name, path.id, user.beyonder.seq.number, user.beyonder.seq.id, **self.log_kwargs)
        return AnswerRedactSeq(user=await self.query_body(), 
                           new=Sequence(seq=user.beyonder.seq_name, number=user.beyonder.seq_number, path=path.name),
                           operation='add')
  
    async def upseq(self, new_seq_number: int | None = None, path_name: str | None = None):
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        if new_seq_number:
            new_seq_number = new_seq_number
            self.check_permission()
        else:
            new_seq_number = user.beyonder.seq_number - 1
        self.check_exist_seq(new_seq_number)
        await user.beyonder.awaitable_attrs.ga
        old_seq = user.beyonder.seq
        old_path = user.beyonder.seq.path
        if user.beyonder.upseq_days > 0 and not self.is_admin:
            raise UpseqNotComeException(upseq_days=user.beyonder.upseq_days)
        if path_name:
            path = await self.dao.path.query_by_name(path_name)
        else:
            path = user.beyonder.seq.path
        if path == None:
            raise PathDontSearchException(path_name=path_name)
        if new_seq_number < 0:
            user.beyonder.ga = path.ga
            new_seq = path.sequences.get(0)
            user.beyonder.seq = new_seq
        else:
            new_seq = path.sequences.get(new_seq_number)
            user.beyonder.seq = new_seq
        user.beyonder.next_upseq = self.get_upseq_time(user.beyonder.seq_number)
        await self.dao.flush()
        self.botlog.upseq(path.name, path.id, user.beyonder.seq.number, user.beyonder.seq.id, new_path_name=old_path.name, new_path_id=old_path.id, new_seq=old_seq.number, new_seq_id=old_seq.id, **self.log_kwargs)
        return AnswerRedactSeq(user=await self.query_body(), 
                           new=Sequence(seq=user.beyonder.seq_name, number=user.beyonder.seq_number, path=path.name),
                           old=Sequence(seq=old_seq.number, number=old_seq.number, path=old_path.name),
                           operation='up')
    
    async def downseq(self, new_seq_number: int | None = None, path_name: str | None = None):
        self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
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
        user.beyonder.next_upseq = self.get_upseq_time(user.beyonder.seq_number)
        await self.dao.flush()
        self.botlog.downseq(path.name, path.id, user.beyonder.seq.number, user.beyonder.seq.id, new_path_name=old_path.name, new_path_id=old_path.id, new_seq=old_seq.number, new_seq_id=old_seq.id, **self.log_kwargs)
        return AnswerRedactSeq(user=await self.query_body(), 
                           new=(Sequence(seq=user.beyonder.seq_name, number=user.beyonder.seq_number, path=path.name) if user.beyonder else None),
                           old=Sequence(seq=old_seq.number, number=old_seq.number, path=old_path.name),
                           operation='down')   

    async def time_info(self):
        user = await self.get_user(is_raise_not_beyonder=True)
        return AnswerTimeInfo(user=await self.query_body(), next_upseq=user.beyonder.next_upseq, last_upseq=user.beyonder.last_upseq, upseq_days=user.beyonder.upseq_days)
    
    async def replace_time(self, new_time: datetime):
        self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        old_time = user.beyonder.next_upseq
        user.beyonder.next_upseq = new_time
        await self.dao.flush()
        self.botlog.time(old_time, new_time, **self.log_kwargs)
        return AnswerTimeReplace(user=await self.query_body(),old_time=old_time, new_time=user.beyonder.next_upseq)
 
    async def edit_time(self, delta: timedelta, operator: str):
        self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        old_time = user.beyonder.next_upseq
        match operator:
            case '-':
                user.beyonder.next_upseq -= delta
            case '+':
                user.beyonder.next_upseq += delta
        await self.dao.flush()
        self.botlog.time(old_time, user.beyonder.next_upseq, **self.log_kwargs)
        return AnswerTimeRedact(user=await self.query_body(),old_time=old_time, new_time=user.beyonder.next_upseq, seconds=delta.total_seconds(), operator=operator)

    async def kill(self):
        if self.purpose_tg_id and not self.purpose_tg_id == self.tg_id:
            self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        old_beyonder = user.beyonder
        user.beyonder = None
        await self.dao.flush()
        self.botlog.kill(old_beyonder.path_name, old_beyonder.seq.path_id, old_beyonder.seq.number, old_beyonder.seq.id, **self.log_kwargs)
        return self.return_query_body(user)