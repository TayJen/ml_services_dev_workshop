from datetime import datetime, timedelta
from typing import Any, Annotated, List, Dict

import os
import time

import pickle
import pandas as pd
from jose import JWTError

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from base_models import Token, TokenData, User
from database import Database

from util.jwt_util import create_access_token, decode_access_token
from util.pwd_util import get_password_hash, verify_password


models = {
    "LogisticRegression": pickle.load(open(os.path.join(os.getcwd(), "models", "lr_model.pkl"), 'rb')),
    "DecisionTreeClassifier": pickle.load(open(os.path.join(os.getcwd(), "models", "tree_model.pkl"), 'rb')),
    "RandomForestClassifier": pickle.load(open(os.path.join(os.getcwd(), "models", "forest_model.pkl"), 'rb'))
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app = FastAPI()
db = Database()

app.mount("/static", StaticFiles(directory="static"), name="static")


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
    return True


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
    file: UploadFile = File(...),
    model_choice: str = "LogisticRegression"
):
    if model_choice not in models:
        return False

    user = db.get_user(username=current_user.username)
    user_id = user.user_id
    user_balance = user.balance

    model_db = db.get_model(model_name=model_choice)
    model_id = model_db.model_id
    model_price = model_db.price
    loaded_model = models.get(model_db.model_name)

    df = pd.read_csv(file.file)
    all_answers = []
    for _, row in df.iterrows():
        if model_price > user_balance:
            break

        start = time.time()
        row_values = row.values
        print(row_values)

        features = dict({col: value for col, value in zip(df.columns, row_values.tolist())})
        print(features)

        data_id = db.insert_new_data(user_id=user_id, **features)

        answer = loaded_model.predict([row_values])[0]
        answer = 1 if answer >= 0.5 else 0

        prediction_time = time.time() - start

        db.insert_prediction(model_id, data_id, prediction_time, answer)

        user_balance -= model_price
        all_answers.append(answer)

    db.update_user_balance(user, user_balance)
    return {"prediction": all_answers}


@app.get("/")
async def home():
    pass


@app.get("/register")
async def register():
    return FileResponse('static/html/register.html')
