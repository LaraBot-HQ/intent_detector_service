from datetime import timedelta

from fastapi import Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
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


class LoginSlack(BaseModel):
    code: str
    state: str


@auth.post("/slack/connect")
async def login_slack_access_token(payload: LoginSlack) -> str:
    auth_code = payload.code
    result = WebClient().oauth_v2_access(
        client_id=config.SLACK_CLIENT_ID,
        client_secret=config.SLACK_CLIENT_SECRET,
        code=auth_code,
        redirect_uri=config.SLACK_REDIRECT_URI
    )

    authed_user = result["authed_user"]

    client_with_token = WebClient(authed_user["access_token"])
    user_info = client_with_token.users_info(user=authed_user["id"])["user"]

    user_info_to_store = {
        "username": user_info["name"],
        "full_name": user_info["real_name"],
        "email": user_info["profile"]["email"],
        "hashed_password": None,
        "disabled": False,
        "slack_data": {
            "bot_access_token": result["access_token"],
            "user_id": authed_user["id"],
            "user_token": authed_user["access_token"],
        }
    }

    fake_users_db[user_info["name"]] = fake_users_db.get(user_info["name"], {}) | user_info_to_store

    return user_info


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
