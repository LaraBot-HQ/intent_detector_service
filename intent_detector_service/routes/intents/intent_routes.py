from fastapi_versioning import version  # type: ignore

from intent_detector_service.config import ALLOWED_LANGUAGE_TYPES
from intent_detector_service.routes.routers import intents
from intent_detector_service.services.detector_factory import DetectorFactory, ALLOWED_ENGINE_TYPES
from intent_detector_service.type_models.request.intent_detection import IntentPayload
from intent_detector_service.type_models.response.intent_detection import IntentResponse


@intents.post("/detect")
@version(1)
async def detect_intention(
    engine: ALLOWED_ENGINE_TYPES,
    language: ALLOWED_LANGUAGE_TYPES,
    payload: IntentPayload
) -> IntentResponse:
    engine_detector = DetectorFactory.construct_detector(language, engine)
    intention_dict = engine_detector.detect_intention(payload.message, payload.actions)
    return IntentResponse.parse_obj(intention_dict)
