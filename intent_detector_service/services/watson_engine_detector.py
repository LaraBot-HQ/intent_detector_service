from fastapi import HTTPException

from intent_detector_service.services.base_intent_detector import IntentEngineDetector, IntentDictionary
from intent_detector_service.type_models.request.intent_detection import ActionObject


class WatsonEngineDetector(IntentEngineDetector):
    NAME = "watson"

    def detect_intention(
        self, user_message: str, actions: list[ActionObject]
    ) -> IntentDictionary:
        raise HTTPException(status_code=404, detail="Engine is not implemented")
