from typing import TypedDict, Union

from fastapi import HTTPException
from azure.cognitiveservices.language.luis.runtime.models import PredictionResponse
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

from intent_detector_service.config import AUTHORING_ENDPOINT, AUTHORING_KEY, LUIS_LANGUAGE_APPS, ALLOWED_LANGUAGE_TYPES
from intent_detector_service.services.base_intent_detector import (
    IntentEngineDetector, IntentDictionary, ExtractedEntityDict
)
from intent_detector_service.type_models.request.intent_detection import ActionObject

if AUTHORING_KEY is None:
    print("Missing AUTHORING_KEY for Luis engine")
    client_runtime = None
else:
    client_runtime = LUISRuntimeClient(AUTHORING_ENDPOINT, CognitiveServicesCredentials(AUTHORING_KEY))

# define app basics


class IntentScoreDict(TypedDict):
    score: float


IntendIdType = Union[str, None]


class PredictionDict(TypedDict):
    top_intent: str  # top entity id
    intents:  dict[IntendIdType, IntentScoreDict]
    entities:  dict[str, dict]


class LuisResponseDict(TypedDict):
    query: str  # user message
    prediction: PredictionDict


class LuisEngineDetector(IntentEngineDetector):
    NAME = "luis"

    def __init__(self, lang: ALLOWED_LANGUAGE_TYPES):
        self.LANG = lang

    def detect_intention(
        self, user_message: str, actions: list[ActionObject]
    ) -> IntentDictionary:
        if client_runtime is None:
            raise HTTPException(status_code=500, detail="Missing LUIS configuration and runtime instance")

        app_id = LUIS_LANGUAGE_APPS.get(self.LANG)

        if not app_id:
            raise HTTPException(status_code=403, detail="There is not a configured app for that language")

        response: PredictionResponse = client_runtime.prediction.get_slot_prediction(
            app_id, 'Production', {"query": user_message.lower().strip().replace("larabot", "")}
        )

        response_dict: LuisResponseDict = response.as_dict()
        prediction_dict = response_dict["prediction"]
        top_intent = prediction_dict["top_intent"]

        action_text = ""
        for action in actions:
            if action.intent_id == top_intent:
                action_text = action.action

        entities = self.extract_entities(prediction_dict)

        return {
            "intent_id": top_intent,
            "action": action_text,
            "entities": entities,
            "similarity": prediction_dict["intents"].get(top_intent, {}).get("score", 0.0), # type: ignore
            "message": user_message
        }

    def extract_entities(
        self, prediction_dict: PredictionDict, *_, **__
    ) -> list[ExtractedEntityDict]:
        return [
            {
                "type": entity,
                "value": ""
            } for entity, ent_dict in prediction_dict["entities"].items()
        ]
