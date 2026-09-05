import loguru, sys, inspect
from functools import wraps
from datetime import time
from typing import Literal

class BotLog:

    def __init__(self, terminal_level: Literal['trace', 'debug', 'info', 'success', 'warning', 'error', 'critical'] = 'debug'):
        self.terminal_level = terminal_level.upper()
        self.loguru = loguru
        self.logger = self.loguru.logger
        self.log_format = """{level.icon}  | <green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan> | <blue>[{extra}]</blue>"""
        self.levels = self.create_levels()
        self.sinks = self.handlers()
        self.create_handlers()

    def handlers(self):
        return [
            {
            'sink':sys.stderr,
            'level':self.levels[0].name,
            'format':self.log_format,
            'enqueue':True,
            }
        ] + [
            {
            "sink":f'logs/{self.levels[0].name.lower()}.log',
            'rotation':'7 day',
            'retention':'30 days',
            'filter':lambda r: r['level'].name == self.levels[0].name,
            'level':self.levels[0].name, 
            'enqueue':True,
            'format':self.log_format,
            'catch':True,
            'serialize':True
            }, 
            {
            "sink":f'logs/api.log',
            'rotation':'7 day',
            'retention':'30 days',
            'level':'DEBUG', 
            'enqueue':True,
            'format':self.log_format,
            'catch':True,
            'serialize':True
            }, 
            {
            "sink":f'logs/warning.log',
            'rotation':'30 day',
            'retention':'120 days',
            'level':'WARNING', 
            'enqueue':True,
            'format':self.log_format,
            'catch':True,
            'serialize':True
            }, 
            {
            "sink":f'logs/error.log',
            'level':'ERROR', 
            'enqueue':True,
            'format':self.log_format,
            'catch':True,
            'serialize':True
            }, 
        ]
    
    def create_handlers(self):
        self.logger.remove()
        id_handlers = []
        for handler in self.sinks:
            l = self.logger.add(**handler)
            id_handlers.append(l)
        return self

    def create_levels(self):
        return [
            self.logger.level("QUERY", no=15, color="<blue>", icon="✉️"),
            self.logger.level("API START", no=25, color="<white>", icon="🏁"),
            self.logger.level("API STOP", no=26, color="<white>", icon="🛑"),
            ]

 
    def decor(self, timer: bool = False, arg: bool = False, logger_kwargs: dict = {}):
        def decorator(func):
            is_async = inspect.iscoroutinefunction(func)
            logger = self.logger.bind(**logger_kwargs, module=func.__module__)
            
            if is_async:
                @wraps(func)
                async def async_wrapped(*args, **kwargs):
                    start_time = time()
                    try:

                        result = await func(*args, **kwargs)
                        end_time = time()

                        log_method = logger.debug if timer else logger.trace
                        log_method(f"Функция {func.__name__} выполнена за {end_time - start_time}")
                        log_method = logger.debug if arg else logger.trace
                        log_method(f"args: {args}, kwargs: {kwargs}")
                        return result
                    except Exception as e:
                        logger.exception(e)
                        raise
                return async_wrapped
            else:
                @wraps(func)
                def sync_wrapped(*args, **kwargs):
                    start_time = time()
                    try:
                        result = func(*args, **kwargs)
                        end_time = time()

                        log_method = logger.debug if timer else logger.trace
                        log_method(f"Функция {func.__name__} выполнена за {end_time - start_time}")
                        log_method = logger.debug if arg else logger.trace
                        log_method(f"args: {args}, kwargs: {kwargs}")
                        return result
                    except Exception as e:
                        logger.exception(e)
                        raise
                return sync_wrapped
        return decorator

    def query(self, url: str, method: str, status_code: int, **kwargs):
        self.logger.log('QUERY', f'{method} {url} {status_code}', **kwargs)
        
    def start(self, **kwargs):
        self.logger.log('API START', f'API запущен', **kwargs)

    def stop(self, **kwargs):
        self.logger.log('API STOP', f'API останавливается', **kwargs)

botlog = BotLog()
log = botlog.logger