from .base import PermissionException,BaseException, BaseExceptionResponse, UserDontFind
from .beyonder import PathDontEnterException, UpseqNotComeException, DontBeyonderException, ALreadyBeyonderException, SeqDontExistException
from .wiki import PathDontSearchException, PathDontEnterFilterException
from .organ import DontMemberError, ALreadyOwnerError, DontEnterPurposeError, ExistRankError, ExistOrganError, InOneOrganError, ALreadyMemberError, OrganPermissioError, OrganPermissionNewRankError, OrganPermissionPurposeRankError, ClosenOrganError, HiddenOrganError

exceptions: list[type[BaseException]] = [
    SeqDontExistException,
    PermissionException,
    UserDontFind,
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
    DontEnterPurposeError
]

exception_codes = {e.status_code:e for e in exceptions}

def get_exception_codes(codes: list[int] | None = None, types:  list[str] | None = None):
    if codes:
        return {k:{'description':v.default_message, 'model':BaseExceptionResponse} for k,v in exception_codes.items() if k in codes} 
    elif types:
        types.append('base')
        return {k:{'description':v.default_message, 'model':BaseExceptionResponse} for k,v in exception_codes.items() if v.type() in types} 
    else:
        return {k:{'description':v.default_message, 'model':BaseExceptionResponse} for k,v in exception_codes.items()} 
