from .base import PermissionException, BaseException, BaseExceptionResponse, UserDontFind, DBError, RedisError
from .beyonder import PathDontEnterException, SeqBusyException, UpseqNotComeException, DontBeyonderException, ALreadyBeyonderException, SeqDontExistException
from .wiki import PathDontSearchException, PathDontEnterFilterException
from .organ import DontMemberError, ALreadyOwnerError, DontEnterPurposeError, ExistRankError, ExistOrganError, InOneOrganError, ALreadyMemberError, OrganPermissioError, OrganPermissionNewRankError, OrganPermissionPurposeRankError, ClosenOrganError, HiddenOrganError
from .logs import DontLogFileException, DontHavePermissionException, DontExistCategoryException
from .newspaper import ExistNewsPaperError, ReaderError, NewsPaperPermissioError
from .setting import ParametrValidateError, ParametrExistError, RankValidateError

exceptions: list[type[BaseException]] = [
    SeqDontExistException,
    PermissionException,
    UserDontFind,
    DBError, 
    RedisError,
    PathDontEnterException,
    PathDontSearchException,
    UpseqNotComeException,
    DontBeyonderException,
    BaseException,
    ALreadyBeyonderException,
    PathDontEnterFilterException,
    DontMemberError, 
    InOneOrganError, 
    ALreadyMemberError, 
    OrganPermissioError, 
    OrganPermissionNewRankError, 
    OrganPermissionPurposeRankError,
    ExistOrganError, 
    ClosenOrganError, 
    HiddenOrganError,
    ExistRankError, 
    ALreadyOwnerError, 
    DontEnterPurposeError,
    ParametrValidateError,
    RankValidateError,
    ParametrExistError,
    SeqBusyException,
    DontLogFileException, 
    DontHavePermissionException, 
    DontExistCategoryException,
    ExistNewsPaperError,
    ReaderError,
    NewsPaperPermissioError
]

exception_codes = {e.status_code:e for e in exceptions}

def get_exception_codes(codes: list[int] | None = None, types: list[str] | None = None):
    base = {PermissionException.status_code:{'description':PermissionException.default_message, 'model':BaseExceptionResponse}}
    if codes:
        return base | {k:{'description':v.default_message, 'model':BaseExceptionResponse} for k,v in exception_codes.items() if k in codes} 
    elif types:    
        return base | {k:{'description':v.default_message, 'model':BaseExceptionResponse} for k,v in exception_codes.items() if v.type() in types} 
    else:
        return {k:{'description':v.default_message, 'model':BaseExceptionResponse} for k,v in exception_codes.items()} 
