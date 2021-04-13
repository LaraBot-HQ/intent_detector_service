from fastapi import APIRouter

ping = APIRouter(
    prefix="/ping",
)

intents = APIRouter(
    prefix="/intents",
)
