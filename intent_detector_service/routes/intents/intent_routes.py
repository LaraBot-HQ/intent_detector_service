from fastapi_versioning import version

from intent_detector_service.routes.routers import intents


@intents.post("/detect")
@version(1)
async def detect_intention() -> dict:
    return {}