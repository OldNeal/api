from app.logic.base import BaseLogic
from datetime import datetime, timedelta
from app.exception.beyonder import SeqDontExistException, UpseqNotComeException, ALreadyBeyonderException, PathDontEnterException
from app.exception.wiki import PathDontSearchException
from app.validate.api.beyonder import (AnswerTimeReplace, 
                                       AnswerTimeRedact, 
                                       AnswerRedactSeq, 
                                       AnswerTimeInfo,
                                       Data)

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

    async def info(self):
        user = await self.get_user(is_raise_not_beyonder=True)
        return AnswerTimeInfo(tg_id=self.purpose_tg_id, next_upseq=user.beyonder.next_upseq, last_upseq=user.beyonder.last_upseq, upseq_days=user.beyonder.upseq_days)
    
    async def drink(self, path_name: str, seq: int = 9):
        if seq < 9:
            self.check_permission()
        self.check_exist_seq(seq)
        user = await self.get_user(self.purpose_tg_id)
        if user.beyonder:
            raise ALreadyBeyonderException(path_name=user.beyonder.path_name, purpose_tg_id=self.purpose_tg_id)
        if path_name == None:
            raise PathDontEnterException()
        path = await self.dao.path.query_by_name(path_name)
        if path == None:
            raise PathDontSearchException(path_name=path_name)
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
        bndr = await self.dao.beyonder.add(new_bndr)
        user.beyonder = bndr
        await self.dao.flush()
        return AnswerRedactSeq(tg_id=self.purpose_tg_id, 
                           new=Data(seq=user.beyonder.seq_name, number=user.beyonder.seq_number, path=path.name),
                           operation='add')
  
    async def upseq(self, add_seq: int = 1, path_name: str | None = None):
        if add_seq > 1:
            self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        self.check_exist_seq(user.beyonder.seq_number - add_seq)
        await user.beyonder.awaitable_attrs.ga
        old_seq = user.beyonder.seq_name
        old_number = user.beyonder.seq_number
        old_path = user.beyonder.seq.path.name
        if user.beyonder.upseq_days > 0 and not self.is_admin:
            raise UpseqNotComeException(upseq_days=user.beyonder.upseq_days)
        if path_name:
            path = await self.dao.path.query_by_name(path_name)
        else:
            path = user.beyonder.seq.path
        if path == None:
            raise PathDontSearchException(path_name=path_name)
        if user.beyonder.seq_number - add_seq < 0:
            user.beyonder.ga = path.ga
            new_seq = path.sequences.get(0)
            user.beyonder.seq = new_seq
        else:
            new_seq = path.sequences.get(user.beyonder.seq_number - add_seq)
            user.beyonder.seq = new_seq
        user.beyonder.next_upseq = self.get_upseq_time(user.beyonder.seq_number)
        await self.dao.flush()
        return AnswerRedactSeq(tg_id=self.purpose_tg_id, 
                           new=Data(seq=user.beyonder.seq_name, number=user.beyonder.seq_number, path=path.name),
                           old=Data(seq=old_seq, number=old_number, path=old_path),
                           operation='up')
    
    async def downseq(self, remove_seq: int = 1, path_name: str | None = None):
        self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        self.check_exist_seq(user.beyonder.seq_number + remove_seq)
        old_seq = user.beyonder.seq_name
        old_number = user.beyonder.seq_number
        old_path = user.beyonder.seq.path.name
        if path_name:
            path = await self.dao.path.query_by_name(path_name)
        else:
            path = user.beyonder.seq.path
        if path == None:
            raise PathDontSearchException(path_name=path_name)
        if user.beyonder.seq_number + remove_seq > 9:
            user.beyonder = None
        else:
            new_seq = path.sequences.get(user.beyonder.seq_number + remove_seq)
            user.beyonder.seq = new_seq
            user.beyonder.ga = None
        user.beyonder.next_upseq = self.get_upseq_time(user.beyonder.seq_number)
        await self.dao.flush()
        return AnswerRedactSeq(tg_id=self.purpose_tg_id, 
                           new=(Data(seq=user.beyonder.seq_name, number=user.beyonder.seq_number, path=path.name) if user.beyonder else None),
                           old=Data(seq=old_seq, number=old_number, path=old_path),
                           operation='down')   
     
    async def replace_time(self, new_time: datetime):
        self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        old_time = user.beyonder.next_upseq
        user.beyonder.next_upseq = new_time
        await self.dao.flush()
        return AnswerTimeReplace(tg_id=self.purpose_tg_id,old_time=old_time, new_time=user.beyonder.next_upseq)
 
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
        return AnswerTimeRedact(tg_id=self.purpose_tg_id,old_time=old_time, new_time=user.beyonder.next_upseq, seconds=delta.total_seconds(), operator=operator)

    async def kill(self):
        if self.purpose_tg_id:
            self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        user.beyonder = None
        await self.dao.flush()
        return True