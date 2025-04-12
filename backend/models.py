from typing import List, Optional

from pydantic import BaseModel


class WordRequest(BaseModel):
    word: str


class ChatRequest(BaseModel):
    message: str


class WordDefinition(BaseModel):
    word: str
    definition: str
    source: str
    image_url: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    definitions: List[WordDefinition]
