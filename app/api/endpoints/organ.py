from fastapi import APIRouter, Depends, Path, Query
from app.validate.api.base import QueryBody, AnswerBaseInfo
from app.api.depends.session import get_session
from app.exception import get_exception_codes
from app.service.organ import OrganService
from app.validate.api.organ import AnswerOrganInfo, AnswerOrganGive, AnswerOrganSettingValues, AnswerAllOrganInfo, AnswerRedactRank, AnswerRedactTitul, AnswerOrganInfoDescription, AnswerOrganInfoMembers, AnswerMemberInfo, QueryOrganSetting, QueryOrganSettingDefault, AnswerOrganSetting

organ_router = APIRouter(prefix='/organ', tags=['organ'], responses=get_exception_codes(types=['organ', 'setting']))

@organ_router.post('/member', response_model=AnswerMemberInfo)
async def organ_member(
                       query: QueryBody, 
                       user_id: int | None = Query(None, description='ID участника'),
                       session = Depends(get_session())
                       ):
    return await OrganService(session, query.user_id, purpose_user_id=user_id).member()

@organ_router.get('/search', response_model=AnswerAllOrganInfo)
async def organ_search(
                       name: str = Query(description='Имя искомой организации'), 
                       session = Depends(get_session())
                       ):
    return await OrganService(session).search(name)
 
@organ_router.post('/info', response_model=AnswerOrganInfo)
async def organ_info(
                         query: QueryBody, 
                         id: int | None = Query(None, description='ID организации'), 
                         member_user_id: int | None = Query(None, description='ID участника'),
                         session = Depends(get_session())
                         ):
    return await OrganService(session, query.user_id, purpose_user_id=member_user_id, organ_id=id).info()

@organ_router.post('/info/members', response_model=AnswerOrganInfoMembers)
async def organ_info_members(
                         query: QueryBody, 
                         id: int | None = Query(None, description='ID организации'),
                         member_user_id: int | None = Query(None, description='ID участника'),
                         session = Depends(get_session())
                         ):
    return await OrganService(session, query.user_id, purpose_user_id=member_user_id, organ_id=id).members()

@organ_router.post('/info/description', response_model=AnswerOrganInfoDescription)
async def organ_info_description(
                         query: QueryBody, 
                         id: int | None = Query(None, description='ID организации'), 
                         member_user_id: int | None = Query(None, description='ID участника'),
                         session = Depends(get_session())
                         ):
    return await OrganService(session, query.user_id, purpose_user_id=member_user_id, organ_id=id).description()

@organ_router.get('/list', response_model=AnswerAllOrganInfo)
async def organ_list(
                         session = Depends(get_session())
                         ):
    return await OrganService(session).list()

@organ_router.get('/top/members', response_model=AnswerAllOrganInfo)
async def organ_top_members(
                      session = Depends(get_session())
                      ):
    return await OrganService(session).organ_top_members()

@organ_router.get('/top/days', response_model=AnswerAllOrganInfo)
async def organ_top_days(
                      session = Depends(get_session())
                      ):
    return await OrganService(session).organ_top_days()

@organ_router.put('/login', response_model=AnswerOrganInfo)
async def organ_login(
                      query: QueryBody, 
                      id: int = Query(description='ID организации'), 
                      session = Depends(get_session())
                      ):
    return await OrganService(session, query.user_id, organ_id=id).login()

@organ_router.post('/exit', response_model=AnswerOrganInfo)
async def organ_exit(
                     query: QueryBody, 
                     session = Depends(get_session())
                     ):
    return await OrganService(session, query.user_id).exit()

@organ_router.put('/create', response_model=AnswerOrganInfo)
async def organ_create(
                       query: QueryBody,
                       name: str = Query(description='Имя новой организации'), 
                       session = Depends(get_session())
                       ):
    return await OrganService(session, query.user_id).create(name)

@organ_router.post('/settings', response_model=AnswerOrganSetting)
async def organ_settings(
                      query: QueryBody, 
                      session = Depends(get_session())
                      ):
    return await OrganService(session, query.user_id).settings()


@organ_router.post('/settings/values', response_model=AnswerOrganSettingValues)
async def organ_settings_values(
                      query: QueryBody, 
                      session = Depends(get_session())
                      ):
    return await OrganService(session, query.user_id).settings_values()

@organ_router.patch('/settings/redact', response_model=AnswerOrganSetting)
async def organ_settings_redact(
                      query: QueryOrganSetting, 
                      session = Depends(get_session())
                      ):
    return await OrganService(session, query.user_id).settings_redact(query.parametrs)


@organ_router.patch('/settings/default', response_model=AnswerOrganSetting)
async def organ_settings_default(
                      query: QueryOrganSettingDefault, 
                      session = Depends(get_session())
                      ):
    return await OrganService(session, query.user_id).settings_default(query.to_default)

@organ_router.post('/capture', response_model=AnswerOrganInfo)
async def organ_capture(
                      query: QueryBody,              
                      session = Depends(get_session())
                      ):
    return await OrganService(session, query.user_id).capture()

@organ_router.patch('/uprank', response_model=AnswerRedactRank)
async def organ_uprank(
                      query: QueryBody, 
                      user_id: int = Query(description='ID пользователя'),
                      rank: int | None = Query(None, description='Новый ранг'),
                      session = Depends(get_session())
                      ):
    return await OrganService(session, query.user_id, purpose_user_id=user_id).uprank(rank)

@organ_router.patch('/downrank', response_model=AnswerRedactRank)
async def organ_downrank(
                      query: QueryBody,                  
                      user_id: int = Query(description='ID пользователя'),
                      rank: int | None = Query(None, description='Новый ранг'),
                      session = Depends(get_session())
                      ):
    return await OrganService(session, query.user_id, purpose_user_id=user_id).downrank(rank)

@organ_router.post('/kick', response_model=AnswerOrganInfo)
async def organ_kick(
                      query: QueryBody, 
                      user_id: int = Query(description='ID пользователя'),
                      session = Depends(get_session())
                      ):
    return await OrganService(session, query.user_id, purpose_user_id=user_id).kick()

@organ_router.patch('/titul/redact', response_model=AnswerRedactTitul)
async def organ_titul_redact(
                      query: QueryBody,      
                      user_id: int = Query(description='ID пользователя'),
                      titul: str = Query(description='Новый титул'),
                      session = Depends(get_session())
                      ):
    return await OrganService(session, query.user_id, purpose_user_id=user_id).titul_redact(titul)

@organ_router.post('/titul/delete', response_model=AnswerRedactTitul)
async def organ_titul_delete(
                      query: QueryBody, 
                      user_id: int = Query(description='ID пользователя'),
                      session = Depends(get_session())
                      ):
    return await OrganService(session, query.user_id, purpose_user_id=user_id).titul_delete()

@organ_router.post('/give', response_model=AnswerOrganGive)
async def organ_give(
                      query: QueryBody, 
                      user_id: int = Query(description='ID пользователя'),
                      session = Depends(get_session())
                      ):
    return await OrganService(session, query.user_id, purpose_user_id=user_id).give()
