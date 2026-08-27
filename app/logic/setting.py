from typing import Literal, Any
from app.validate.logic.setting import OrganSettingValidate, SettingGroupValidate, SettingParametrValidate
from app.db.models.organ import OrganDB

NOT_DEFAULT = object()

class SettingParametr:
    def __init__(self,
                tag: str,
                name: str,
                group: Literal['main', 'permission', 'appearance'],
                type: str,
                emodzi: str | None = None,
                custom_emodzi_id: str | None = None,
                description: str | None = None,
                default_value = None,
                converter = lambda x: x,
                is_redact: bool = True,
                is_hidden: bool = False,
                ):
        self.tag = tag
        self.name = name
        self.group = group
        self.emodzi = emodzi
        self.type = type
        self.custom_emodzi_id = custom_emodzi_id
        self.description = description
        self.default_value = default_value
        self.converter = converter
        self.value = None
        self.is_default_value: bool | None = None
        self.is_redact = is_redact
        self.is_hidden = is_hidden

    def update(self, data: dict[str, Any]):
        if self.is_redact:
            self.value = self.converter(data.get(self.tag, self.default_value if self.default_value != NOT_DEFAULT else None))
        self.is_default_value = not bool(data.get(self.tag))
        return self

    def model_dump(self):
        return self.validate.model_dump()

    def to_default(self):
        return self.update({})

    @property
    def validate(self):
        return SettingParametrValidate.model_validate(self)

    @property
    def is_not_default(self):
        return self.default_value is NOT_DEFAULT

is_hidden_organ = SettingParametr('hidden', 'Видимость организации', 'main', 'bool', emodzi='🔍', default_value=False)
is_closen_organ = SettingParametr('closen', 'Приватный вход', 'main', 'bool', emodzi='🚪', default_value=False)
start_rank = SettingParametr('start_rank', 'Стартовый ранг', 'main', 'int', emodzi='🏁', default_value=9)
min_rank = SettingParametr('min_rank', 'Минимальный ранг', 'main', 'int', emodzi='➖', default_value=9)
max_rank = SettingParametr('max_rank', 'Максимальный ранг', 'main', 'int', emodzi='➕', default_value=0)

name = SettingParametr('name', 'Название', 'appearance', 'str', emodzi='🏷️', default_value=NOT_DEFAULT)
emodzi = SettingParametr('emodzi', 'Эмодзи', 'appearance', 'str', emodzi='🙂')
custom_emodzi_id = SettingParametr('custom_emodzi_id', 'ID кастомного эмодзи', 'appearance', 'str', emodzi='🆔', is_hidden=True)
description = SettingParametr('description', 'Описание', 'appearance', 'str', emodzi='📖')
rank_names = SettingParametr('rank_names', 'Названия рангов', 'appearance', 'dict', emodzi='🔖', default_value=OrganDB.default_rank_name(), is_hidden=True)

redact_rank = SettingParametr('redact_rank', 'Изменять ранг', 'permission', 'int', emodzi='🎎', default_value=0)
redact_titul = SettingParametr('redact_titul', 'Изменять титул', 'permission', 'int', emodzi='🪪', default_value=0)
kick = SettingParametr('kick', 'Выгонять', 'permission', 'int', '⛓️‍💥', default_value=0)
redact_setting = SettingParametr('redact_setting', 'Редактирование настроек', 'permission', 'int', emodzi='⚙️', default_value=0)

class SettingGroup:
    def __init__(self,
                tag: Literal['main', 'permission', 'appearance'],
                name: str,
                parametrs: list[SettingParametr],
                emodzi: str | None = None,
                custom_emodzi_id: str | None = None,
                description: str | None = None,
                ):
        self.tag = tag
        self.name = name
        self.parametrs = parametrs
        self.emodzi = emodzi
        self.custom_emodzi_id = custom_emodzi_id
        self.description = description

    @property
    def parametr_tags(self):
        return [p.tag for p in self.parametrs]

    def get_parametr(self, tag: str):
        return {p.tag:p for p in self.parametrs}.get(tag)

    def update(self, data: dict[str, Any]):
        [p.update(data) for p in self.parametrs]
        return self

    def get(self, tag: str, default_value = None):
        return getattr(self.get_parametr(tag), 'value', default_value)

    @property
    def validate(self):
        return SettingGroupValidate.model_validate(self)
    
    def model_dump(self):
        return self.validate.model_dump()

    def to_default(self):
        return [p.to_default() for p in self.parametrs if p.is_not_default]

    @property
    def not_default_parametrs(cls):
        return [p.tag for p in cls.parametrs if p.is_not_default]
    
group_main = SettingGroup('main', 'Основные', [is_hidden_organ, is_closen_organ, start_rank])
group_permission = SettingGroup('permission', 'Права', [kick, redact_titul, redact_rank, redact_setting])
group_appearance = SettingGroup('appearance', 'Внешний вид', [name, emodzi, custom_emodzi_id, description, rank_names])

class OrganSetting:
    main = group_main
    permission = group_permission
    appearance = group_appearance
    groups = [main, permission, appearance]
    group_tags = {g.tag:g for g in groups}

    @classmethod
    def parametrs(cls):
        return cls.main.parametrs + cls.appearance.parametrs + cls.permission.parametrs
    
    @classmethod
    def not_default_parametrs(cls):
        return [p.tag for p in cls.parametrs() if p.is_not_default]

    def __init__(self, data: dict[str, Any]):
        self.data = data
        self.update(data)
  
    def update(self, data: dict[str, Any]):
        [g.update(data) for g in self.groups]
        return self
        
    @property
    def validate(self):
        return OrganSettingValidate(groups=self.groups)

    def model_dump(self):
        return self.validate.model_dump()

    def model_dump_db(self, is_default_value: bool = False):
        return {p.tag:p.value for p in self.parametrs() if p.is_default_value == is_default_value}

    @property
    def values(self):
        return {p.tag:p.value for p in self.parametrs()}

    def to_default(self, group: str | None = None):
        if group:
            self.group_tags.get(group).to_default()
        else:
            [g.to_default() for g in self.groups]
        return self.model_dump_db()