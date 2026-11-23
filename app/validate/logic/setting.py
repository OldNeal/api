from app.validate.logic.base import BaseLogicValidate
from typing import Literal, Any

class SettingParametrValidate(BaseLogicValidate):
    tag: str
    name: str
    group: Literal['main', 'permission', 'appearance']
    type: str
    emodzi: str | None = None
    custom_emodzi_id: str | None = None
    description: str | None = None
    value: bool | str | int | dict | None = None
    is_default_value: bool
    is_redact: bool = True
    is_hidden: bool = False

class SettingGroupValidate(BaseLogicValidate):
    tag: Literal['main', 'permission', 'appearance']
    name: str
    emodzi: str | None = None
    custom_emodzi_id: str | None = None
    description: str | None = None
    parametrs: list[SettingParametrValidate]

class OrganSettingValidate(BaseLogicValidate):
    groups: list[SettingGroupValidate]