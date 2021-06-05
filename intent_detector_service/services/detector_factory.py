from typing import Literal, Type

from intent_detector_service.config import ALLOWED_LANGUAGE_TYPES
from intent_detector_service.services.base_intent_detector import IntentEngineDetector
from intent_detector_service.services.local_intent_detector import LocalEngineDetector
from intent_detector_service.services.luis_engine_detector import LuisEngineDetector
from intent_detector_service.services.watson_engine_detector import WatsonEngineDetector


class UnknownDetectorError(Exception):
    pass


ALLOWED_ENGINE_TYPES = Literal["watson", "luis", "local"]


class DetectorFactory:

    detector_classes: dict[ALLOWED_ENGINE_TYPES, Type[IntentEngineDetector]] = {
        "watson": WatsonEngineDetector,
        "luis": LuisEngineDetector,
        "local": LocalEngineDetector,
    }

    @classmethod
    def construct_detector(
        cls, language: ALLOWED_LANGUAGE_TYPES, detector_type: Literal["watson", "luis", "local"]
    ) -> IntentEngineDetector:
        if cls.detector_classes.get(detector_type):
            return cls.detector_classes[detector_type](language)

        raise UnknownDetectorError(f"there is not a detector engine for {detector_type}")
