from fastapi import APIRouter, Depends, Path, Query
from app.validate.api.base import QueryBody, AnswerBaseInfo
from app.api.depends.session import get_session
from app.exception import get_exception_codes
from app.service.organ import OrganService
from app.validate.api.organ import AnswerOrganInfo, AnswerOrganGive, AnswerOrganSettingValues, AnswerAllOrganInfo, AnswerRedactRank, AnswerRedactTitul, AnswerOrganInfoDescription, AnswerOrganInfoMembers, AnswerMemberInfo, QueryOrganSetting, QueryOrganSettingDefault, AnswerOrganSetting

organ_router = APIRouter(prefix='/organ', tags=['organ'], responses=get_exception_codes(types=['organ']))

@organ_router.post('/member', tags=['organ'], operation_id='organ_member', response_model=AnswerMemberInfo)
async def organ_member(
                       query: QueryBody, 
                       tg_id: int | None = Query(None, description='ID участника'), 
                       session = Depends(get_session())
                       ):
    data = await OrganService(session, query.tg_id, purpose_tg_id=tg_id).member()
    return data

@organ_router.get('/search', tags=['organ'], operation_id='organ_search', response_model=AnswerAllOrganInfo)
async def organ_search(
                       name: str = Query(description='Имя искомой организации'), 
                       session = Depends(get_session())
                       ):
    data = await OrganService(session).search(name)
    return data

@organ_router.post('/info', tags=['organ'], operation_id='organ_info', response_model=AnswerOrganInfo)
async def organ_info(
                         query: QueryBody, 
                         id: int | None = Query(None, description='ID организации'), 
                         member_tg_id: int | None = Query(None, description='ID участника'), 
                         session = Depends(get_session())
                         ):
    data = await OrganService(session, query.tg_id, purpose_tg_id=member_tg_id, organ_id=id).info()
    return data

@organ_router.post('/info/members', tags=['organ'], operation_id='organ_info_members', response_model=AnswerOrganInfoMembers)
async def organ_info_members(
                         query: QueryBody, 
                         id: int | None = Query(None, description='ID организации'),
                         member_tg_id: int | None = Query(None, description='ID участника'), 
                         session = Depends(get_session())
                         ):
    data = await OrganService(session, query.tg_id, purpose_tg_id=member_tg_id, organ_id=id).members()
    return data

@organ_router.post('/info/description', tags=['organ'], operation_id='organ_info_description', response_model=AnswerOrganInfoDescription)
async def organ_info_description(
                         query: QueryBody, 
                         id: int | None = Query(None, description='ID организации'), 
                         member_tg_id: int | None = Query(None, description='ID участника'), 
                         session = Depends(get_session())
                         ):
    data = await OrganService(session, query.tg_id, purpose_tg_id=member_tg_id, organ_id=id).description()
    return data

@organ_router.get('/list', tags=['organ'], operation_id='organ_list', response_model=AnswerAllOrganInfo)
async def organ_list(
                         session = Depends(get_session())
                         ):
    data = await OrganService(session).list()
    return data

@organ_router.get('/top/members', tags=['organ'], operation_id='organ_top_members', response_model=AnswerAllOrganInfo)
async def organ_top_members(
                      session = Depends(get_session())
                      ):
    data = await OrganService(session).organ_top_members()
    return data

@organ_router.get('/top/days', tags=['organ'], operation_id='organ_top_days', response_model=AnswerAllOrganInfo)
async def organ_top_days(
                      session = Depends(get_session())
                      ):
    data = await OrganService(session).organ_top_days()
    return data

@organ_router.put('/login', tags=['organ'], operation_id='organ_login', response_model=AnswerOrganInfo)
async def organ_login(
                      query: QueryBody, 
                      id: int = Query(description='ID организации'), 
                      session = Depends(get_session())
                      ):
    data = await OrganService(session, query.tg_id, organ_id=id).login()
    return data

@organ_router.post('/exit', tags=['organ'], operation_id='organ_exit', response_model=AnswerOrganInfo)
async def organ_exit(
                     query: QueryBody, 
                     session = Depends(get_session())
                     ):
    data = await OrganService(session, query.tg_id).exit()
    return data

@organ_router.put('/create', tags=['organ'], operation_id='organ_create', response_model=AnswerOrganInfo)
async def organ_create(
                       query: QueryBody,
                       name: str = Query(description='Имя новой организации'), 
                       session = Depends(get_session())
                       ):
    data = await OrganService(session, query.tg_id).create(name)
    return data

@organ_router.post('/settings', tags=['organ'], operation_id='organ_settings', response_model=AnswerOrganSetting)
async def organ_settings(
                      query: QueryBody, 
                      session = Depends(get_session())
                      ):
    data = await OrganService(session, query.tg_id).settings()
    return data


@organ_router.post('/settings/values', tags=['organ'], operation_id='organ_settings_values', response_model=AnswerOrganSettingValues)
async def organ_settings_values(
                      query: QueryBody, 
                      session = Depends(get_session())
                      ):
    data = await OrganService(session, query.tg_id).settings_values()
    return data

@organ_router.patch('/settings/redact', tags=['organ'], operation_id='organ_settings_redact', response_model=AnswerOrganSetting)
async def organ_settings_redact(
                      query: QueryOrganSetting, 
                      session = Depends(get_session())
                      ):
    data = await OrganService(session, query.tg_id).settings_redact(query.parametrs)
    return data


@organ_router.patch('/settings/default', tags=['organ'], operation_id='organ_settings_default', response_model=AnswerOrganSetting)
async def organ_settings_default(
                      query: QueryOrganSettingDefault, 
                      session = Depends(get_session())
                      ):
    data = await OrganService(session, query.tg_id).settings_default(query.to_default)
    return data

@organ_router.post('/capture', tags=['organ'], operation_id='organ_capture', response_model=AnswerOrganInfo)
async def organ_capture(
                      query: QueryBody,              
                      session = Depends(get_session())
                      ):
    data = await OrganService(session, query.tg_id).capture()
    return data

@organ_router.patch('/uprank', tags=['organ'], operation_id='organ_uprank', response_model=AnswerRedactRank)
async def organ_uprank(
                      query: QueryBody, 
                      tg_id: int = Query(description='Telegram ID пользователя'),
                      rank: int | None = Query(None, description='Новый ранг'),
                      session = Depends(get_session())
                      ):
    data = await OrganService(session, query.tg_id, purpose_tg_id=tg_id).uprank(rank)
    return data

@organ_router.patch('/downrank', tags=['organ'], operation_id='organ_downrank', response_model=AnswerRedactRank)
async def organ_downrank(
                      query: QueryBody,                  
                      tg_id: int = Query(description='Telegram ID пользователя'),
                      rank: int | None = Query(None, description='Новый ранг'),
                      session = Depends(get_session())
                      ):
    data = await OrganService(session, query.tg_id, purpose_tg_id=tg_id).downrank(rank)
    return data

@organ_router.post('/kick', tags=['organ'], operation_id='organ_kick', response_model=AnswerOrganInfo)
async def organ_kick(
                      query: QueryBody, 
                      tg_id: int = Query(description='Telegram ID пользователя'),                
                      session = Depends(get_session())
                      ):
    data = await OrganService(session, query.tg_id, purpose_tg_id=tg_id).kick()
    return data

@organ_router.patch('/titul/redact', tags=['organ'], operation_id='organ_titul_redact', response_model=AnswerRedactTitul)
async def organ_titul_redact(
                      query: QueryBody,      
                      tg_id: int = Query(description='Telegram ID пользователя'),            
                      titul: str = Query(description='Новый титул'),
                      session = Depends(get_session())
                      ):
    data = await OrganService(session, query.tg_id, purpose_tg_id=tg_id).titul_redact(titul)
    return data

@organ_router.post('/titul/delete', tags=['organ'], operation_id='organ_titul_delete', response_model=AnswerRedactTitul)
async def organ_titul_delete(
                      query: QueryBody, 
                      tg_id: int = Query(description='Telegram ID пользователя'),                
                      session = Depends(get_session())
                      ):
    data = await OrganService(session, query.tg_id, purpose_tg_id=tg_id).titul_delete()
    return data

@organ_router.post('/give', tags=['organ'], operation_id='organ_give', response_model=AnswerOrganGive)
async def organ_give(
                      query: QueryBody, 
                      tg_id: int = Query(description='Telegram ID пользователя'),                
                      session = Depends(get_session())
                      ):
    data = await OrganService(session, query.tg_id, purpose_tg_id=tg_id).give()
    return data

