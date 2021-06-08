from typing import NamedTuple, TypedDict, Union, Protocol, Final

from intent_detector_service.config import ALLOWED_LANGUAGE_TYPES
from intent_detector_service.type_models.request.intent_detection import ActionObject


class SimilarityObject(NamedTuple):
    action_object: ActionObject
    action: str
    similarity: float
    position: int


class ExtractedEntityDict(TypedDict):
    type: str
    value: Union[str, int, float]


class IntentDictionary(TypedDict):
    intent_id: str
    action: str
    entities: list[ExtractedEntityDict]
    similarity: float
    message: str


class IntentEngineDetector(Protocol):
    LANG: ALLOWED_LANGUAGE_TYPES
    NAME: str

    def __init__(self, lang: ALLOWED_LANGUAGE_TYPES):
        self.LANG = lang

    def detect_intention(
        self, user_message: str, actions: list[ActionObject]
    ) -> IntentDictionary:
        ...
