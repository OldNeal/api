from app.logic.base import BaseLogic
from datetime import datetime, timedelta

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
    async def info(self):
        user = await self.get_user()
        return user.beyonder
    
    async def drink(self, path_name: str, seq: int = 9):
        if seq < 9:
            self.check_permission()
        if seq > 9 or seq < -1:
            raise
        user = await self.get_user(self.purpose_tg_id)
        path = await self.dao.path.query_by_name(path_name)
        new_bndr = {
            'seq':path.sequences.get(seq), 
            'user_id':user.id, 
            'last_upseq':datetime.now(), 
            'next_upseq':datetime.now()+timedelta(days=upseq_time.get(seq))
            } 
        if seq == -1:
            new_bndr |= {
                'ga':path.ga,
                'seq':path.sequences.get(0), 
            }
        self.dao.beyonder.add(new_bndr)
  
    async def upseq(self, add_seq: int = 1):
        if add_seq > 1:
            self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        if user.beyonder.seq.number - add_seq < -1:
            raise
        if user.beyonder.upseq_days > 0 and not self.is_admin:
            raise
        if user.beyonder.seq.number - add_seq == 0:
            await user.beyonder.awaitable_attrs.ga
            user.beyonder.ga = user.beyonder.seq.path.ga
        else:
            new_seq = user.beyonder.seq.path.sequences.get(user.beyonder.seq.number - add_seq)
            user.beyonder.seq = new_seq
        return user.beyonder
    
    async def downseq(self, remove_seq: int = 1):
        self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        if user.beyonder.seq.number + remove_seq > 9:
            raise
        elif user.beyonder.seq.number + remove_seq == 9:
            user.beyonder = None
        else:
            new_seq = user.beyonder.seq.path.sequences.get(user.beyonder.seq.number + remove_seq)
            user.beyonder.seq = new_seq
            await user.beyonder.awaitable_attrs.ga
            user.beyonder.ga = None
        return user.beyonder    
    
    async def replace_time(self, new_time: datetime):
        self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        user.beyonder.next_upseq = new_time
        return
 
    async def edit_time(self, delta: timedelta, operator: str):
        self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        match operator:
            case '-':
                user.beyonder.next_upseq -= delta
            case '+':
                user.beyonder.next_upseq -= delta
        return user.beyonder

    async def kill(self):
        if self.purpose_tg_id:
            self.check_permission()
        user = await self.get_user(self.purpose_tg_id, is_raise_not_beyonder=True)
        user.beyonder = None
        return user.beyonder