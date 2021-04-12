from fastapi_versioning import version
from pydantic import BaseModel

from intent_detector_service.routes.routers import intents


class IntentPayload(BaseModel):
    message: str
    actions: list[str]


@intents.post("/detect")
@version(1)
async def detect_intention(engine: str) -> dict:
    return {}
