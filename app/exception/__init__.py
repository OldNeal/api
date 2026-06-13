from .base import PermissionException, BaseException, BaseExceptionResponse
from .beyonder import PathDontEnterException, UpseqNotComeException, DontBeyonderException, ALreadyBeyonderException, SeqDontExistException
from .wiki import PathDontSearchException, PathDontEnterFilterException

exceptions: list[type[BaseException]] = [
    SeqDontExistException,
    PermissionException,
    PathDontEnterException,
    PathDontSearchException,
    UpseqNotComeException,
    DontBeyonderException,
    BaseException,
    ALreadyBeyonderException,
    PathDontEnterFilterException
]

exception_codes = {e.status_code:e for e in exceptions}

def get_exception_codes(codes: list[int] | None = None, types:  list[str] | None = None):
    if codes:
        return {k:{'description':v.default_message, 'model':BaseExceptionResponse} for k,v in exception_codes.items() if k in codes} 
    elif types:
        return {k:{'description':v.default_message, 'model':BaseExceptionResponse} for k,v in exception_codes.items() if v.type() in types} 
    else:
        return {k:{'description':v.default_message, 'model':BaseExceptionResponse} for k,v in exception_codes.items()} 
