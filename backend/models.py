from typing import List

from pydantic import BaseModel


class WordRequest(BaseModel):
    word: str


class ChatRequest(BaseModel):
    message: str


class Definition(BaseModel):
    word: str
    definition: str
    source: str

class ChatResponse(BaseModel):
    reply: str
    definitions: List[Definition]
