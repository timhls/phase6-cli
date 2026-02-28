from pydantic import BaseModel
from typing import Optional, List


class SubjectIdOwner(BaseModel):
    id: str
    ownerId: str


class SubjectContent(BaseModel):
    name: str
    description: Optional[str] = None
    bookName: Optional[str] = None
    primaryLang: Optional[str] = None
    secondaryLang: Optional[str] = None


class Subject(BaseModel):
    subjectId: SubjectIdOwner
    subjectContent: SubjectContent


class CardContent(BaseModel):
    question: str
    answer: str
    questionExample: Optional[str] = None
    answerExample: Optional[str] = None
    questionTranscription: Optional[str] = None
    answerTranscription: Optional[str] = None
    questionAnswerId: Optional[str] = None
    unitIdToOwner: Optional[dict] = None
    subjectIdToOwner: Optional[dict] = None


class CardProgress(BaseModel):
    active: bool
    isDue: bool
    phase: int
    dueDate: Optional[str] = None
    practicedDate: Optional[str] = None


class VocabItem(BaseModel):
    cardIdString: str
    normal: Optional[CardProgress] = None
    opposite: Optional[CardProgress] = None
    cardContent: Optional[CardContent] = None


class VocabList(BaseModel):
    items: List[VocabItem]
