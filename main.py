from datetime import datetime, timedelta, timezone
from typing import Any, List, Dict
from typing import Annotated

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import FileResponse

from forms import UserRegisterForm

SECRET_KEY = "b521d3d1b56fe661b177afb0a1fbb7f1b054aa7473956739d5a2a8f93b8d9bcf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "hashed_password": "",
    },
}

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def register_user(fake_db, username: str, full_name: str, password: str):
    user = get_user(fake_db, username)
    if user:
        return False
    hashed_password = get_password_hash(password)
    new_user = {
        "username": username,
        "full_name": full_name,
        "hashed_password": hashed_password,
    }
    fake_users_db[username] = new_user
    print(fake_users_db)

    return True


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/login/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
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
    return Token(access_token=access_token, token_type="bearer")


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


@app.post("/register/")
async def register_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    full_name = "NOT IMPLEMENTED"
    if not register_user(fake_users_db, form_data.username, full_name, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )






# models_list = [{"id": 1, "name": "LogisticRegression"},
#                {"id": 2, "name": "DecisionTree"},
#                {"id": 3, "name": "RandomForest"},
#                {"id": 4, "name": "XGBoost"}]


# http://127.0.0.1:8000/
# @app.get("/")
# def index():
#     return {"message": "Hello World!"}


# @app.get("/models")
# def read_models() -> List[Dict[str, Any]]:
#     """
#         Получение списка моделей
#         :params: None
#         :return: list of dicts with models ids and names
#     """
#     return models_list


# @app.get("/models/{model_id}")
# def read_model(model_id: int):
#     for model in models_list:
#         if model["id"] == model_id:
#             return model
#     return {"message": f"Model with id {model_id} was not found"}
