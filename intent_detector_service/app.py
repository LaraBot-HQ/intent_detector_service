from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI

from intent_detector_service.routes.routers import intents

app = FastAPI(
    title="Intent detector service",
    description="This service handles the detection of an intent when "
    "we need to relate it to a previous intention",
)

app.include_router(intents)

app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/api_v{major}",
    description="This service handles the detection of an intent when "
    "we need to relate it to a previous intention",
)
