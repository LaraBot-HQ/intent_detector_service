from typing import Literal, Protocol, TypedDict, Type


class UnknownDetectorError(Exception):
    pass


class IntentDictionary(TypedDict):
    intent: str
    entities: list[str]


class IntentEngineDetector(Protocol):
    NAME: str

    def detect_intention(
        self, user_message: str, actions: list[str]
    ) -> IntentDictionary:
        ...


class WatsonEngineDetector(IntentEngineDetector):
    NAME = "watson"

    def detect_intention(
        self, user_message: str, actions: list[str]
    ) -> IntentDictionary:
        return {"intent": "", "entities": []}


class LuisEngineDetector(IntentEngineDetector):
    NAME = "luis"

    def detect_intention(
        self, user_message: str, actions: list[str]
    ) -> IntentDictionary:
        return {"intent": "", "entities": []}


class LocalEngineDetector(IntentEngineDetector):
    """
    This is the intent detector for local working using spacy and NLTK
    """

    NAME = "local"

    def detect_intention(
        self, user_message: str, actions: list[str]
    ) -> IntentDictionary:
        return {"intent": "", "entities": []}


class DetectorFactory:

    detector_classes: dict[str, Type[IntentEngineDetector]] = {
        "watson": WatsonEngineDetector,
        "luis": LuisEngineDetector,
        "local": LocalEngineDetector,
    }

    def construct_detector(
        self, detector_type: Literal["watson", "luis", "local"]
    ) -> IntentEngineDetector:
        if self.detector_classes.get(detector_type):
            return self.detector_classes[detector_type]()

        raise UnknownDetectorError(f"there is not a detector for {detector_type}")
