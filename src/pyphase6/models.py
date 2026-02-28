from pydantic import BaseModel
from typing import Optional, List


class VocabItem(BaseModel):
    id: Optional[str] = None
    question: str
    answer: str
    phase: Optional[int] = None
    # We will refine this once we know the actual JSON structure


class VocabList(BaseModel):
    items: List[VocabItem]
