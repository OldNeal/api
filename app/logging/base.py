import loguru, sys, inspect
from functools import wraps
from datetime import time
from typing import Literal

def log_filter(no: int):
    return lambda r: r['level'].no == no

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
            "sink":f'logs/base/{self.levels[0].name.lower()}' + '_{time:YYYY-MM-DD}.log',
            'rotation':'7 day',
            'retention':'30 days',
            'filter':log_filter(self.levels[0].no),
            'level':self.levels[0].name, 
            'enqueue':True,
            'format':self.log_format,
            'catch':True,
            'serialize':True
            }, 
            {
            "sink":f'logs/base/api' + '_{time:YYYY-MM-DD}.log',
            'rotation':'7 day',
            'retention':'30 days',
            'level':'DEBUG', 
            'enqueue':True,
            'format':self.log_format,
            'catch':True,
            'serialize':True
            }, 
            {
            "sink":f'logs/base/warning' + '_{time:YYYY-MM-DD}.log',
            'rotation':'30 day',
            'retention':'120 days',
            'level':'WARNING', 
            'enqueue':True,
            'format':self.log_format,
            'catch':True,
            'serialize':True
            }, 
            {
            "sink":f'logs/base/error' + '_{time:YYYY-MM-DD}.log',
            'level':'ERROR', 
            'enqueue':True,
            'format':self.log_format,
            'catch':True,
            'serialize':True
            }, 
        ] + [
            {
            "sink":f'logs/beyonder/{beyonder_logs.name.lower()}' + '_{time:YYYY-MM-DD}.log',
            'filter':log_filter(beyonder_logs.no),
            'level':f'{beyonder_logs.name}', 
            'enqueue':True,
            'format':self.log_format,
            'catch':True,
            'serialize':True
            } for beyonder_logs in self.beyonder_handlers
        ]
    
    def create_handlers(self):
        self.logger.remove()
        id_handlers = []
        for handler in self.sinks:
            l = self.logger.add(**handler)
            id_handlers.append(l)
        return self


    def create_levels(self):
        self.base_handlers = self.create_levels_base()
        self.beyonder_handlers = self.create_levels_bndr() 
        self.organ_handlers = self.create_levels_organ()
        return self.base_handlers + self.beyonder_handlers + self.organ_handlers

    def create_levels_base(self):
        return [
            self.logger.level("QUERY", no=15, color="<blue>", icon="✉️"),
            self.logger.level("API START", no=1, color="<white>", icon="🏁"),
            self.logger.level("API STOP", no=2, color="<white>", icon="🛑")
            ]

    def create_levels_bndr(self):
        return [
            self.logger.level("DRINK", no=21, color="<light-green>", icon="🧪"),
            self.logger.level("UPSEQ", no=22, color="<light-green>", icon="🔼"),
            self.logger.level("DOWNSEQ", no=23, color="<light-green>", icon="🔽"),
            self.logger.level("KILL", no=24, color="<light-green>", icon="☠️"),
            self.logger.level("TIME", no=25, color="<light-green>", icon="⌛")
            ]

    def create_levels_organ(self):
        return [
            self.logger.level("ORGAN CREATE", no=31, color="<yellow>", icon="➕"),
            self.logger.level("ORGAN LOGIN", no=32, color="<yellow>", icon="🚪"),
            self.logger.level("ORGAN RANK", no=33, color="<yellow>", icon="🎎"),
            self.logger.level("ORGAN KICK", no=34, color="<yellow>", icon="🚪"),
            self.logger.level("ORGAN EXIT", no=35, color="<yellow>", icon="🚪"),
            self.logger.level("ORGAN TITUL", no=36, color="<yellow>", icon="🎖️"),
            self.logger.level("ORGAN SETTING", no=37, color="<yellow>", icon="⚙️"),
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

    def drink(self, path_name: str, path_id: int, seq: int, seq_id: int, **kwargs):
        self.logger.log(
            'DRINK', f'Стал потустороним пути {path_name}, выпив зелье {seq} последовательности', 
            **kwargs | {'path_name':path_name, 'path_id':path_id, 'seq':seq, 'seq_id': seq_id})

    def upseq(self, 
              old_path_name: str, old_path_id: int, old_seq: int, old_seq_id: int, 
              new_path_name: str, new_path_id: int, new_seq: int, new_seq_id: int,
              **kwargs
              ):
        self.logger.log(
            'UPSEQ', f'Повысил последовательность с {old_seq} на {new_seq}{f', поменяв путь {old_path_name} на {new_path_name}' if old_path_id != new_path_id else ''}', 
            **kwargs | {
                'old_path_name':old_path_name, 'old_path_id':old_path_id, 'old_seq':old_seq, 'old_seq_id': old_seq_id, 
                'new_path_name':new_path_name, 'new_path_id':new_path_id, 'new_seq':new_seq, 'new_seq_id': new_seq_id
                })

    def downseq(self, 
              old_path_name: str, old_path_id: int, old_seq: int, old_seq_id: int, 
              new_path_name: str, new_path_id: int, new_seq: int, new_seq_id: int,
              **kwargs
              ):
        self.logger.log(
            'DOWNSEQ', f'Понизили последовательность с {old_seq} на {new_seq}{f', поменяв путь {old_path_name} на {new_path_name}' if old_path_id != new_path_id else ''}', 
            **kwargs | {
                'old_path_name':old_path_name, 'old_path_id':old_path_id, 'old_seq':old_seq, 'old_seq_id': old_seq_id, 
                'new_path_name':new_path_name, 'new_path_id':new_path_id, 'new_seq':new_seq, 'new_seq_id': new_seq_id
                })

    def kill(self, old_path_name: str, old_path_id: int, old_seq: int, old_seq_id: int, **kwargs):
        self.logger.log(
            'KILL', f'Потерял контроль', 
            **kwargs | {'old_path_name':old_path_name, 'old_path_id':old_path_id, 'old_seq':old_seq, 'old_seq_id': old_seq_id})

    def time(self, old_time: str, new_time: str, **kwargs):
        self.logger.log(
            'DRINK', f'Изменено время продвижения: {old_time} >>> {new_time}', 
            **kwargs | {'old_time':old_time, 'new_time': new_time})



    def organ_create(self, organ_name: str, organ_id: int, **kwargs):
        self.logger.log(
            'ORGAN CREATE', f'Создал организацию {organ_name}', 
            **kwargs | {'organ_name':organ_name, 'organ_id': organ_id})

    def organ_login(self, organ_name: str, organ_id: int, **kwargs):
        self.logger.log(
            'ORGAN LOGIN', f'Вошёл в организацию {organ_name}', 
            **kwargs | {'organ_name':organ_name, 'organ_id': organ_id})

    def organ_rank(self, organ_name: str, organ_id: int, old_rank: int, new_rank: int, **kwargs):
        self.logger.log(
            'ORGAN RANK', f'Изменил ранг: {old_rank} >>> {new_rank}', 
            **kwargs | {'organ_name':organ_name, 'organ_id': organ_id, 'old_rank':old_rank, 'new_rank': new_rank})

    def organ_kick(self, organ_name: str, organ_id: int, old_rank: int, **kwargs):
        self.logger.log(
            'ORGAN KICK', f'Выгнали из организации', 
            **kwargs | {'organ_name':organ_name, 'organ_id': organ_id, 'old_rank':old_rank})

    def organ_exit(self, organ_name: str, organ_id: int, old_rank: int, **kwargs):
        self.logger.log(
            'ORGAN EXIT', f'Вышел из организации', 
            **kwargs | {'organ_name':organ_name, 'organ_id': organ_id, 'old_rank':old_rank})

    def organ_titul(self, organ_name: str, organ_id: int, old_titul: str | None = None, new_titul: str | None = None, **kwargs):
        if new_titul and old_titul:
            self.logger.log(
                'ORGAN TITUL', f'Изменили титул: "{old_titul}" >>> "{new_titul}"', 
                **kwargs | {'organ_name':organ_name, 'organ_id': organ_id, 'old_titul':old_titul, 'new_titul':new_titul})
        elif old_titul:
            self.logger.log(
                'ORGAN TITUL', f'Титул отнят', 
                **kwargs | {'organ_name':organ_name, 'organ_id': organ_id, 'old_titul':old_titul, 'new_titul':new_titul})
        elif new_titul:
            self.logger.log(
                'ORGAN TITUL', f'Дан титул "{new_titul}"', 
                **kwargs | {'organ_name':organ_name, 'organ_id': organ_id, 'old_titul':old_titul, 'new_titul':new_titul})

    def organ_setting(self, organ_name: str, organ_id: int, old_setting: dict, new_setting: dict, **kwargs):
        self.logger.log(
            'ORGAN SETTING', f'Изменили настройки', 
            **kwargs | {'organ_name':organ_name, 'organ_id': organ_id, 'old_setting':old_setting, 'new_setting':new_setting})
                
    def organ_setting_default(self, organ_name: str, organ_id: int, old_setting: dict, **kwargs):
        self.logger.log(
            'ORGAN SETTING', f'Сбросили настройки', 
            **kwargs | {'organ_name':organ_name, 'organ_id': organ_id, 'old_setting':old_setting})
        
botlog = BotLog()
log = botlog.logger