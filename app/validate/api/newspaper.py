from app.validate.api.base import AnswerBody, AnswerBaseBody, QueryBody, ReaderInfo, ForButtons, Page
from app.validate.logic.setting import OrganSettingValidate
from app.validate.api.organ import OrganSettingDefault

class AnswerNewsPaperInfoBase(AnswerBaseBody):
    id: int
    name: str

class AnswerReaderInfo(AnswerBody):
    reader: ReaderInfo | None = None
    for_buttons: ForButtons | None = None

class NewsPaperInfo(AnswerNewsPaperInfoBase):
    owner: AnswerReaderInfo | None = None
    emodzi: str | None = None
    custom_emodzi_id: str | None = None
    reader_counts: int = 0

class AnswerNewsPaperInfo(AnswerBody):
    news_paper: NewsPaperInfo
    for_buttons: ForButtons | None = None

class AnswerNewsPaperInfoReaders(AnswerNewsPaperInfoBase, AnswerBody):
    readers: list[AnswerReaderInfo]
    page: Page | None = None
    count: int = 0

class AnswerNewsPaperInfoDescription(AnswerNewsPaperInfoBase, AnswerBody):
    description: str | None = None

class AnswerAllNewsPaperInfo(AnswerBaseBody):
    search_value: str | None = None
    news_papers: list[NewsPaperInfo]
    page: Page | None = None
    count: int = 0

class AnswerRedactRank(AnswerBody):
    news_paper: NewsPaperInfo
    new_rank: int
    old_rank: int

class AnswerNewsPaperSettingValues(AnswerBody):
    values: dict

class AnswerNewsPaperSetting(AnswerBody):
    settings: OrganSettingValidate

class AnswerNewsPaperGive(AnswerBody):
    pass

class QueryNewsPaperSetting(QueryBody):
    parametrs: dict

class QueryNewsPaperSettingDefault(QueryBody):
    to_default: OrganSettingDefault