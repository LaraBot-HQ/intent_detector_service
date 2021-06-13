from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI  # type: ignore

from intent_detector_service.config import ALLOW_ORIGINS
from intent_detector_service.routes.routers import intents, ping, auth

app = FastAPI(
    title="Intent detector service",
    description="This service handles the detection of an intent when "
    "we need to relate it to a previous intention",
)

app.include_router(ping)
app.include_router(intents)
app.include_router(auth)

app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/api_v{major}",
    description="This service handles the detection of an intent when "
    "we need to relate it to a previous intention",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
