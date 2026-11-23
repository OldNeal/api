from .base import PermissionException, BaseException, BaseExceptionResponse, TokenDontFind, RedisError, CoreError, CoreTimeoutError

exceptions: list[type[BaseException]] = [
    PermissionException,
    TokenDontFind,
    RedisError,
    BaseException,
    CoreError,
    CoreTimeoutError
]

exception_codes = {e.status_code:e for e in exceptions}

def get_exception_codes(codes: list[int] | None = None, types: list[str] | None = None):
    base = {PermissionException.status_code:{'description':PermissionException.default_message, 'model':PermissionException.model_response}}
    if codes:
        return base | {k:{'description':v.default_message, 'model':v.model_response} for k,v in exception_codes.items() if k in codes} 
    elif types:    
        return base | {k:{'description':v.default_message, 'model':v.model_response} for k,v in exception_codes.items() if v.type() in types} 
    else:
        return {k:{'description':v.default_message, 'model':v.model_response} for k,v in exception_codes.items()} 
