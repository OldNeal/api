from app.validate.api.base import AnswerBody, AnswerUserBody, QueryBody, ReaderInfo, ForButtons
from app.validate.logic.setting import OrganSettingValidate
from app.validate.api.organ import OrganSettingDefault

class AnswerNewsPaperInfoBase(AnswerBody):
    id: int
    name: str

class AnswerReaderInfo(AnswerUserBody):
    reader: ReaderInfo | None = None
    for_buttons: ForButtons | None = None

class NewsPaperInfo(AnswerNewsPaperInfoBase):
    owner: AnswerReaderInfo | None = None
    emodzi: str | None = None
    custom_emodzi_id: str | None = None
    reader_counts: int = 0

class AnswerNewsPaperInfo(AnswerUserBody):
    news_paper: NewsPaperInfo
    for_buttons: ForButtons | None = None

class AnswerNewsPaperInfoReaders(AnswerNewsPaperInfoBase, AnswerUserBody):
    readers: list[AnswerReaderInfo]

class AnswerAllNewsPaperInfo(AnswerBody):
    search_value: str | None = None
    news_papers: list[NewsPaperInfo]

class AnswerRedactRank(AnswerUserBody):
    news_paper: NewsPaperInfo
    new_rank: int
    old_rank: int

class AnswerNewsPaperSettingValues(AnswerUserBody):
    values: dict

class AnswerNewsPaperSetting(AnswerUserBody):
    settings: OrganSettingValidate

class AnswerNewsPaperGive(AnswerUserBody):
    purpose: AnswerReaderInfo

class QueryNewsPaperSetting(QueryBody):
    parametrs: dict

class QueryNewsPaperSettingDefault(QueryBody):
    to_default: OrganSettingDefault