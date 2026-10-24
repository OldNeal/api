import json
from typing import Callable, Any
from pathlib import PurePath
from pydantic import Field
from app.validate.logic.setting import (
    BaseLogicValidate,
    OrganSettingValidate,
    SettingGroupValidate,
    SettingParametrValidate,
)
from app.exception.setting import ParametrValidateError, RankValidateError, ParametrExistError
from app.db.models.organ import OrganDB

PARAMETRS_JSON_PATH = PurePath('app') / PurePath('logic') / PurePath('setting') / PurePath('parametrs.json')

def is_int(x, parametr_tag):
    if type(x) is int:
        return x
    raise ParametrValidateError(parametr_tag=parametr_tag, value=x, parametr_type='числом')

def is_str(x, parametr_tag):
    if type(x) is str:
        return x
    raise ParametrValidateError(parametr_tag=parametr_tag, value=x, parametr_type='строкой')

def is_dict(x, parametr_tag):
    if type(x) is dict:
        return x
    raise ParametrValidateError(parametr_tag=parametr_tag, value=x, parametr_type='словарем')

def is_bool(x, parametr_tag):
    if type(x) is bool:
        return x
    raise ParametrValidateError(parametr_tag=parametr_tag, value=x, parametr_type='bool-типа')

def check_rank_names(x: dict[str, str], parametr_tag, max_rank: int, min_rank: int):
    is_dict(x, parametr_tag)
    for k, v in x.items():
        is_str(k, parametr_tag)
        if not k.isdigit():
            raise ParametrValidateError(parametr_tag=parametr_tag, value=x, parametr_type='числом')
        else:
            if not (min_rank <= int(k) <= max_rank):
                raise RankValidateError(parametr_tag=parametr_tag, value=x, max_rank=max_rank, min_rank=min_rank)
        is_str(v, parametr_tag)
    default_names = OrganDB.default_rank_name()
    return default_names | x

def check_rank_exist(x, parametr_tag, max_rank: int, min_rank: int):
    x = is_int(x, parametr_tag)
    if not (min_rank <= x <= max_rank):
        raise RankValidateError(parametr_tag=parametr_tag, value=x, max_rank=max_rank, min_rank=min_rank)
    return x

converters =  [is_bool, is_dict, is_int, is_str, check_rank_names, check_rank_exist]
converter_names = {c.__name__:c for c in converters}

class SettingParametr(BaseLogicValidate):
    tag: str
    group: str
    type: str
    default_value: Any = None
    have_default_value: bool = True
    converter_name: str | None = Field(default=None, alias='converter')
    value: Any = None
    is_default_value: bool | None = None
    kwargs: dict = {}

    @property
    def converter(self) -> Callable[[Any, str], Any]:
        return converter_names.get(self.converter_name, lambda x, parametr_tag: x)

    def update(self, data: dict[str, Any]):
        parametr = data.get(self.tag, self.default_value if self.have_default_value else None)
        self.value = self.converter(parametr, self.tag, **self.kwargs) if not parametr is None else None
        self.is_default_value = self.tag not in data or self.value is None or self.value == self.default_value
        return self

    def to_default(self):
        return self.update({})

    @property
    def is_not_default(self):
        return not self.have_default_value

GROUP_NAMES = {
    'main': 'Основные',
    'permission': 'Права',
    'appearance': 'Внешний вид',
}
PARAMETR_NAMES = {
    'hidden': 'Видимость организации',
    'closen': 'Приватный вход',
    'start_rank': 'Стартовый ранг',
    'min_rank': 'Минимальный ранг',
    'max_rank': 'Максимальный ранг',
    'name': 'Название',
    'emodzi': 'Эмодзи',
    'custom_emodzi_id': 'ID кастомного эмодзи',
    'description': 'Описание',
    'rank_names': 'Названия рангов',
    'redact_rank': 'Изменять ранг',
    'redact_titul': 'Изменять титул',
    'kick': 'Выгонять',
    'redact_setting': 'Редактирование настроек',
}

#is_hidden_organ = SettingParametr('hidden', 'Видимость организации', 'main', 'bool', emodzi='🔍', default_value=False, converter=is_bool)
#is_closen_organ = SettingParametr('closen', 'Приватный вход', 'main', 'bool', emodzi='🚪', default_value=False, converter=is_bool)
#start_rank = SettingParametr('start_rank', 'Стартовый ранг', 'main', 'int', emodzi='🏁', default_value=9, converter=is_int)
#min_rank = SettingParametr('min_rank', 'Минимальный ранг', 'main', 'int', emodzi='➖', default_value=9, converter=is_int)
#max_rank = SettingParametr('max_rank', 'Максимальный ранг', 'main', 'int', emodzi='➕', default_value=0, converter=is_int)
#
#name = SettingParametr('name', 'Название', 'appearance', 'str', emodzi='🏷️', have_default_value=False, converter=is_str)
#emodzi = SettingParametr('emodzi', 'Эмодзи', 'appearance', 'str', emodzi='🙂', converter=is_str)
#custom_emodzi_id = SettingParametr('custom_emodzi_id', 'ID кастомного эмодзи', 'appearance', 'str', emodzi='🆔', is_hidden=True, converter=is_str)
#description = SettingParametr('description', 'Описание', 'appearance', 'str', emodzi='📖', converter=is_str)
#rank_names = SettingParametr('rank_names', 'Названия рангов', 'appearance', 'dict', emodzi='🔖', default_value=OrganDB.default_rank_name(), is_hidden=True, converter=check_rank_names)
#
#redact_rank = SettingParametr('redact_rank', 'Изменять ранг', 'permission', 'int', emodzi='🎎', default_value=0, converter=is_int)
#redact_titul = SettingParametr('redact_titul', 'Изменять титул', 'permission', 'int', emodzi='🪪', default_value=0, converter=is_int)
#kick = SettingParametr('kick', 'Выгонять', 'permission', 'int', '⛓️‍💥', default_value=0, converter=is_int)
#redact_setting = SettingParametr('redact_setting', 'Редактирование настроек', 'permission', 'int', emodzi='⚙️', default_value=0, converter=is_int)

class Setting:
    type: str | None = None

    def __init__(self, data: dict[str, Any]):
        self.data = data
        self._parametrs = [
            parametr.model_copy(deep=True)
            for parametr in self.get_parametrs()
            if parametr.type == self.type
        ]
        self.parametr_tags = [p.tag for p in self._parametrs]
        self.update(data)

    @classmethod
    def get_parametrs(self):
        with open(PARAMETRS_JSON_PATH, encoding='UTF-8') as file:
            return [SettingParametr.model_validate(p) for p in json.loads(file.read())]

    @property
    def parametrs(self) -> list[SettingParametr]:
        return self._parametrs

    @property
    def groups(self) -> dict[str, list[SettingParametr]]:
        groups: dict[str, list[SettingParametr]] = {}
        for parametr in self.parametrs:
            groups.setdefault(parametr.group, []).append(parametr)
        return groups

    def get_group(self, group: str) -> dict[str, Any]:
        return {
            parametr.tag: parametr.value
            for parametr in self.groups.get(group, [])
        }

    @property
    def main(self) -> dict[str, Any]:
        return self.get_group('main')

    @property
    def permission(self) -> dict[str, Any]:
        return self.get_group('permission')

    @property
    def appearance(self) -> dict[str, Any]:
        return self.get_group('appearance')

    @property
    def validate(self) -> OrganSettingValidate:
        groups = [
            SettingGroupValidate(
                tag=group,
                name=GROUP_NAMES[group],
                parametrs=[
                    SettingParametrValidate(
                        tag=parametr.tag,
                        name=PARAMETR_NAMES.get(parametr.tag, parametr.tag),
                        group=parametr.group,
                        type=parametr.type,
                        value=parametr.value,
                        is_default_value=bool(parametr.is_default_value),
                    )
                    for parametr in parametrs
                ],
            )
            for group, parametrs in sorted(
                self.groups.items(),
                key=lambda item: list(GROUP_NAMES).index(item[0]),
            )
        ]
        return OrganSettingValidate(groups=groups)

    def check_tag(self, data: dict[str, Any]):
        for tag in data.keys():
            if not tag in self.parametr_tags:
                raise ParametrExistError(parametr_tag=tag)

    def update(self, data: dict[str, Any]):
        self.check_tag(data)
        for parametr in self.parametrs:
            parametr.update(data)
        self.data = data
        return self

    def model_dump_db(self, is_default_value: bool = False):
        return {
            parametr.tag: parametr.value
            for parametr in self.parametrs
            if parametr.is_default_value == is_default_value
        }

    @property
    def values(self):
        return {parametr.tag: parametr.value for parametr in self.parametrs}

    def to_default(self, group: str | None = None):
        if group is not None:
            parametrs = self.groups.get(group)
            if parametrs is None:
                raise ValueError(f'Unknown setting group: {group}')
            for parametr in parametrs:
                if parametr.is_not_default:
                    parametr.to_default()
        else:
            for parametr in self.parametrs:
                if parametr.is_not_default:
                    parametr.to_default()
        return self.model_dump_db()

class OrganSetting(Setting):
    type = 'organ'

class NewsPaperSetting(Setting):
    type = 'news_paper'