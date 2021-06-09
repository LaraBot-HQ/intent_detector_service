from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from slack import WebClient

from intent_detector_service import config
from intent_detector_service.routes.routers import auth
from intent_detector_service.services.oauth import (
    authenticate_user, fake_users_db, Token, ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token, get_user_by_username, UserPayload, create_user
)


@auth.post("/create_user")
async def create_user_endpoint(user_data: UserPayload) -> str:
    if get_user_by_username(user_data.username):
        raise HTTPException(status_code=403, detail="That username is already in used")

    create_user(user_data)

    return "success"


@auth.post("/slack/callback", response_model=Token)
async def login_for_access_token(auth_code: str) -> str:
    result = WebClient().oauth_v2_access(
        client_id=config.SLACK_CLIENT_ID,
        client_secret=config.SLACK_CLIENT_SECRET,
        code=auth_code,
        redirect_uri=config.SLACK_REDIRECT_URI
    )

    authed_user = result["authed_user"]

    fake_users_db[authed_user["id"]] = {
        "slack_access_token": authed_user["access_token"]
    }

    return "success"


@auth.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}