from typing import Union

from pydantic import BaseModel


class ExtractedEntity(BaseModel):
    type: str
    value: Union[str, int, float]


class IntentResponse(BaseModel):
    intent_id: str
    action: str
    entities: list[ExtractedEntity]
    similarity: float
    message: str
