from datetime import datetime, timedelta
from typing import Any, Annotated, List, Dict

import base64
from jose import JWTError

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import FileResponse

from base_models import Token, TokenData, User
from database import Database

from util.jwt_util import create_access_token, decode_access_token
from util.pwd_util import get_password_hash, verify_password



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app = FastAPI()
db = Database()


def register_user(username: str, password: str):
    user = db.get_user(username)
    if user:
        return False

    hashed_password = get_password_hash(password)
    new_user = {
        "username": username,
        "hashed_password": hashed_password,
    }
    db.insert_new_user(**new_user)

    return True


def authenticate_user(username: str, password: str):
    user = db.get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@app.post("/login/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/register/")
async def register_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    if not register_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        print('Successfully registered')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.post("/predict/")
async def predict(
    current_user: Annotated[User, Depends(get_current_active_user)],
    data: str
):
    data_csv = base64.b64decode(data)
    
    