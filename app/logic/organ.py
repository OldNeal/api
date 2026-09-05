from app.logic.base import BaseLogic
from app.validate.api.organ import AnswerOrganInfo, AnswerOrganGive, OrganInfo, ForButtons, AnswerAllOrganInfo, AnswerRedactRank, AnswerOrganSetting, AnswerOrganSettingValues, AnswerRedactTitul, AnswerOrganInfoDescription, AnswerOrganInfoMembers, AnswerMemberInfo, OrganSettingDefault, MemberInfo, UserDB
from app.db.models.organ import MemberDB, OrganDB
from app.db.models.main import UserDB
from app.logic.setting import OrganSetting
from app.exception.organ import DontMemberError, DontEnterPurposeError, ExistRankError, ALreadyOwnerError, ExistOrganError, InOneOrganError, ALreadyMemberError, OrganPermissioError, OrganPermissionNewRankError, HiddenOrganError, ClosenOrganError, OrganPermissionPurposeRankError

class OrganLogic(BaseLogic):
    def __init__(self, session, tg_id: int | None = None, purpose_tg_id: int | None = None, organ_id: int | None = None, is_admin: bool = False):
        super().__init__(session, tg_id, purpose_tg_id, is_admin)
        self.organ_id = organ_id

    def boolean(self, *args, func, **kwargs):
        try:
            return bool(func(*args, **kwargs | {'to_print':False}))
        except:
            return False

    def is_member(self, user: UserDB, to_print: bool = True):
        if user.member is None:
            raise DontMemberError(tg_id=user.tg_id, to_print=to_print)
        return user

    def is_not_member(self, user: UserDB, to_print: bool = True):
        if user.member:
            raise ALreadyMemberError(tg_id=user.tg_id, to_print=to_print)
        return user

    def is_enter_purpose(self, user: UserDB, purpose: UserDB | None = None, to_print: bool = True):
        if purpose is None or user.tg_id == purpose.tg_id:
            raise DontEnterPurposeError(to_print=to_print)
        return user, purpose
    
    def is_permission(self, user: UserDB, tag: str, to_print: bool = True):
        setting = OrganSetting(user.member.organ.setting)
        if user.member.rank > setting.permission.get(tag, 0):
            raise OrganPermissioError(rank=user.member.rank, to_print=to_print)
        return user, setting

    def is_hidden(self, user: UserDB, organ: OrganDB, to_print: bool = True):
        setting = OrganSetting(organ.setting)
        if setting.main.get('hidden') and not (user.member and user.member.organ_id == organ.id):
            raise HiddenOrganError(to_print=to_print)
        return setting
    
    def is_closen(self, organ: OrganDB, to_print: bool = True):
        setting = OrganSetting(organ.setting)
        if setting.main.get('closen'):
            raise ClosenOrganError(to_print=to_print)
        return setting

    def is_exist_rank(self, rank: int | None, organ: OrganDB, to_print: bool = True):
        setting = OrganSetting(organ.setting)
        if rank and not(setting.main.get('min_rank', 9) >= rank >= setting.main.get('max_rank', 0)):
            raise ExistRankError(rank=rank, to_print=to_print)
        return setting
        
    def is_rank(self, user: UserDB, purpose: UserDB, new_purpose_rank: int | None = None, to_print: bool = True):
        self.in_one_organ(user, purpose)
        self.is_enter_purpose(user, purpose)
        if user.member.rank >= purpose.member.rank:
            raise OrganPermissionPurposeRankError(to_print=to_print)
        if new_purpose_rank and user.member.rank >= new_purpose_rank or user.member.rank >= purpose.member.rank - 1:
            raise OrganPermissionNewRankError(to_print=to_print)
        return user, purpose

    def in_one_organ(self, user: UserDB, purpose: UserDB, to_print: bool = True):
        if user.member.organ_id != user.member.organ_id:
            raise InOneOrganError(to_print=to_print)
        return user, purpose

    def is_owner(self, user: UserDB, to_print: bool = True):
        if user.member.rank != 0:
            raise OrganPermissioError(to_print=to_print)
        return user

    def is_capture(self, owner: AnswerMemberInfo | None, to_print: bool = True):
        if owner:
            raise OrganPermissioError(owner_id=owner.user.tg_id, to_print=to_print)
        return True
    

    async def check_is_member(self, tg_id: int | None = None):
        user = await self.get_user(tg_id)
        return self.is_member(user)

    async def check_is_not_member(self, tg_id: int | None = None):
        user = await self.get_user(tg_id)
        return self.is_not_member(user)

    async def check_permission(self, tag: str):
        user = await self.check_is_member(self.tg_id)
        return self.is_permission(user, tag)

    async def check_rank(self, user: UserDB, new_purpose_rank: int):
        purpose = await self.get_user()
        return self.is_rank(user, purpose, new_purpose_rank)

    async def check_exist_organ(self, organ_id: int):
        organ = await self.get_organ(organ_id)
        if organ is None:
            raise ExistOrganError()
        return organ

    async def check_organ_admin_permission(self, tag: str, new_rank: int | None = None):
        user, setting = await self.check_permission(tag)
        purpose = await self.get_user()
        self.is_rank(user, purpose, new_rank)
        return user, purpose

    async def check_capture(self):
        user = await self.check_is_member()
        owner = await self.get_owner()
        if owner and owner.user.tg_id == user.tg_id:
            raise ALreadyOwnerError()
        self.is_capture(owner)
        return user

    async def check_give(self):
        user = await self.check_is_member(self.tg_id)
        purpose = await self.check_is_member()
        self.is_owner(user)
        self.is_enter_purpose(user, purpose)
        return self.in_one_organ(user, purpose)




    async def get_organ(self, id: int | None = None):
        return await self.dao.organ.query_by_id(id or self.organ_id)

    async def get_owner(self, organ_id: int | None = None):
        owner = await self.dao.user.get_organ_owner_by_organ_id(organ_id or self.organ_id)
        return await self.return_owner_info(owner)

    async def return_owner_info(self, owner: UserDB):
        return await self.return_member_info(owner, add_for_buttons=False) if owner else None

    async def return_member_info(self, user: UserDB, purpose: UserDB | None = None, add_for_buttons: bool = True):
        purpose = purpose or user
        return AnswerMemberInfo(
            user=self.return_query_body(purpose),
            member=(MemberInfo(
                    titul=purpose.member.titul,
                    organ_name=purpose.member.organ.name,
                    organ_id=purpose.member.organ.id,
                    rank=purpose.member.rank,
                    rank_name=purpose.member.rank_name,
                    login_at=purpose.member.created_at.isoformat()
                ) if purpose.member else None),
            for_buttons=(await self.return_for_buttons(user) if add_for_buttons else None)
            )

    async def return_organ_info(self, user: UserDB, organ: OrganDB):
        return AnswerOrganInfo(
            user=self.return_query_body(user),
            organ=OrganInfo(
                id=organ.id,
                name=organ.name,
                owner=await self.get_owner(organ.id),
                emodzi=organ.emodzi,
                custom_emodzi_id=organ.custom_emodzi_id,
                member_counts=len(organ.members),
                created_at=organ.created_at.isoformat()
                ),
            for_buttons=await self.return_for_buttons(user, organ.id)
            )

    async def return_for_buttons(self, user: UserDB, organ_id: int | None = None):
        owner = await self.get_owner(organ_id or self.organ_id)
        return ForButtons(
                is_member=self.boolean(user, func=self.is_member),
                organ_id=user.member.organ_id if user.member else organ_id,
                is_redact_setting=self.boolean(user, 'redact_setting', func=self.is_permission),
                is_redact_rank=self.boolean(user, 'redact_rank', func=self.is_permission),
                is_redact_titul=self.boolean(user, 'redact_titul', func=self.is_permission),
                is_kick=self.boolean(user, 'kick', func=self.is_permission),
                is_capture=self.boolean(owner, func=self.is_capture),
                is_give=self.boolean(user, func=self.is_owner)
            )

    async def return_organs_info(self, organs: list[OrganDB]):
        return [OrganInfo(
            id=organ.id,
            name=organ.name,
            owner=await self.get_owner(organ.id),
            emodzi=organ.emodzi,
            custom_emodzi_id=organ.custom_emodzi_id,
            member_counts=len(organ.members),
            created_at=organ.created_at.isoformat()
        ) for organ in organs]


    async def member(self):
        user = await self.get_user(only_user=True)
        purpose = await self.check_is_member()
        return await self.return_member_info(user, purpose)

    async def info(self, id: int | None = None):
        user = await self.get_user()
        organ = await self.check_exist_organ(id or self.organ_id or self.is_member(user).member.organ_id)
        self.is_hidden(user, organ)
        return await self.return_organ_info(user, organ)

    async def members(self, id: int | None = None):
        user = await self.get_user()
        organ = await self.check_exist_organ(id or self.organ_id or self.is_member(user).member.organ_id)
        self.is_hidden(user, organ)
        return AnswerOrganInfoMembers(
            user=self.return_query_body(user),
            id=organ.id,
            name=organ.name,
            members=[await self.return_member_info(user, mbr) for mbr in await self.dao.user.get_members_by_organ_id(organ.id)]
        )
    
    async def description(self, id: int | None = None):
        user = await self.get_user()
        organ = await self.check_exist_organ(id or self.organ_id or self.is_member(user).member.organ_id)
        self.is_hidden(user, organ)
        return AnswerOrganInfoDescription(
            user=self.return_query_body(user),
            id=organ.id,
            name=organ.name,
            description=organ.description
        )

    async def search(self, name: str):
        organs = await self.dao.organ.search_by_name(name)
        return AnswerAllOrganInfo(
            search_value=name,
            organs=await self.return_organs_info(organs)
        )

    async def list(self):
        organs = await self.dao.organ.find_all()
        return AnswerAllOrganInfo(
            organs=await self.return_organs_info(organs)
        )

    async def organ_top_members(self):
        organs = await self.dao.organ.find_all()
        return AnswerAllOrganInfo(
            organs=await self.return_organs_info(sorted(organs, key=lambda x: len(x.members), reverse=True)[:6])
        )

    async def organ_top_days(self):
        organs = await self.dao.organ.find_all()
        return AnswerAllOrganInfo(
            organs=await self.return_organs_info(sorted(organs, key=lambda x: x.created_at)[:6])
        )


        
    async def login(self):
        user = await self.check_is_not_member()
        organ = await self.check_exist_organ(self.organ_id)
        setting = self.is_closen(organ)
        organ.members.append(MemberDB(user_id=user.id, organ_id=organ.id, rank=setting.main.get('start_rank')))
        await self.dao.flush()
        return await self.return_organ_info(user, organ)
    
    async def exit(self):
        user = await self.check_is_member()
        organ = await self.get_organ(user.member.organ_id)
        organ.members.remove(user.member)
        await self.dao.commit()
        return await self.return_organ_info(user, organ)
    
    async def create(self, name: str):
        user = await self.check_is_not_member()
        organ = await self.dao.organ.add({'name':name})
        organ.members.append(MemberDB(user_id=user.id, organ_id=organ.id, rank=0))
        await self.dao.flush()
        return await self.return_organ_info(user, organ)
 
    async def settings(self):
        user, setting = await self.check_permission('redact_setting')
        return AnswerOrganSetting(user=self.return_query_body(user), settings=setting.validate)
    
    async def settings_values(self):
        user, setting = await self.check_permission('redact_setting')
        return AnswerOrganSettingValues(user=self.return_query_body(user), values=setting.values)

    async def settings_redact(self, parametrs: dict):
        user, setting = await self.check_permission('redact_setting')
        user.member.organ.setting = setting.update(parametrs).model_dump_db()
        self.dao.organ.update_obj(user.member.organ, user.member.organ.setting)
        return AnswerOrganSetting(user=self.return_query_body(user), settings=setting.validate)
    
    async def settings_default(self, default: OrganSettingDefault):
        user, setting = await self.check_permission('redact_setting')
        if default.is_all:
            setting.to_default()
            user.member.organ.setting = {}
            user.member.organ.description = None
            user.member.organ.emodzi = None
            user.member.organ.custom_emodzi_id = None
        elif default.group == OrganSetting.appearance.tag:
            user.member.organ.setting = setting.to_default(default.group)
            default_setting = setting.model_dump_db(True)
            default_setting.pop('name')
            self.dao.organ.update_obj(user.member.organ, default_setting)
        elif default.group:
            user.member.organ.setting = setting.to_default(default.group)
        elif default.parametr:
            user.member.organ.setting.pop(default.parametr)
        else:
            raise
        await self.dao.flush()
        return AnswerOrganSetting(user=self.return_query_body(user), settings=setting.validate)



    
    async def rank_redact(self, operation: str, rank: int | None = None):
        user, purpose = await self.check_organ_admin_permission('redact_rank', rank)
        self.is_enter_purpose(user, purpose)
        self.is_exist_rank(rank, user.member.organ)
        old_rank = purpose.member.rank
        if rank:
            purpose.member.rank = rank
        elif operation == 'up':
            purpose.member.rank -= 1
        elif operation == 'down':
            purpose.member.rank += 1
        self.is_exist_rank(purpose.member.rank, user.member.organ)
        await self.dao.flush()
        return AnswerRedactRank(user=self.return_query_body(purpose), new_rank=purpose.member.rank, old_rank=old_rank)
    
    async def kick(self):
        user, purpose = await self.check_organ_admin_permission('kick')
        self.is_enter_purpose(user, purpose)
        organ = user.member.organ
        await purpose.member.organ.awaitable_attrs.members
        purpose.member.organ.members.remove(purpose.member)
        await self.dao.flush()
        return await self.return_organ_info(purpose, organ)
    
    async def titul_redact(self, titul: str | None = None):
        user, purpose = await self.check_organ_admin_permission('redact_titul')
        self.is_enter_purpose(user, purpose)
        old_titul = purpose.member.titul
        purpose.member.titul = titul
        await self.dao.flush()
        return AnswerRedactTitul(user=self.return_query_body(purpose), new_titul=titul, old_titul=old_titul)

    async def capture(self):
        user = await self.check_capture()
        user.member.rank = 0
        await self.dao.flush()
        return await self.info()
    
    async def give(self):
        user, purpose = await self.check_give()
        user.member.rank = 1
        purpose.member.rank = 0
        await self.dao.flush()
        return AnswerOrganGive(
            user=await self.query_body(self.tg_id),
            purpose=await self.return_member_info(user, purpose)
        )
