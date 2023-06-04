"""
Date : 2023.04.28
Author : 서하민

FastApi practice app



"""

"""
https://velog.io/@idj7183/Fast-API-%ED%99%9C%EC%9A%A9-2

important!

"""

# run web page ->  uvicorn main:app --reload        ## main->file name  // app->app name


from fastapi import FastAPI, Request, Form, Depends, HTTPException, status, Response
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Annotated, Union
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from pydantic import BaseModel
from collections import OrderedDict
import json


#added
from fastapi.middleware.cors import CORSMiddleware
##





#--- JWT setting ---#
# to get a string like this run:
# openssl rand -hex 32
#must change befor live service
SECRET_KEY = "b992da1f01e3bea4ed5e0a0b9e8ed6dab31fa0ce022bc1c147f9a0cc53a59357" #must change befor live service
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    userType: str
    username: str
    email: str
    profilePicture: Union[str, None] = None
    disabled: bool


class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()



templets = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")



#added
origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

##


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def authenticate_user(userInfo, username: str, password: str):
    user = get_user(userInfo, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    user = get_user(userInfo, username=token_data.username)#changed
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



#------#





#---database---#

# user1 is test account
# user1:2345

# userType = admin or user / username = nickname / hashed_password / email = email address / profilePicture = user profile picture 
userInfo = {"admin":{"userType":"admin", "username":"admin", "hashed_password":"$2b$12$qVvSlFz6todXOw5U2h8waurQrIVqmvnMBAXU3A0HvAVxTH.vkbMKm","email":"email1111@aaaaaa.com", "profilePicture":"admin.png", "disabled":False},
            "user1":{"userType":"user", "username":"user1",  "hashed_password":"$2b$12$9j.mP0Z42NrsMzLlkmYawOAte048jVVwadHNi.oCVOIzM8rIZs/QC","email":"email2222@bbbbbb.com", "profilePicture":"user1.png", "disabled":False}
        }
#------#



#token
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(userInfo, form_data.username, form_data.password)
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
    print(form_data.username, form_data.password)
    print(f"[{datetime.utcnow()}]\n",{"access_token": access_token, "token_type": "bearer"})

    fileData = OrderedDict()
    fileData["acces_tokken"] = access_token
    fileData["token_type"] = "bearer"

    return {"access_token": access_token, "token_type": "bearer"}
    #return json.dumps(fileData, ensure_ascii=False, indent="\t")



@app.get("/", response_class=HTMLResponse)
def first(request:Request):
    return templets.TemplateResponse("home.html", {"request":request})

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user


#login page html show
@app.get("/login", response_class=HTMLResponse) #login page
async def login(request:Request):
    return templets.TemplateResponse("index.html", {"request":request})

"""
#token login processing, return token
@app.post("/loginProcess", response_model=Token)
async def login_to_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(userInfo, form_data.username, form_data.password)
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
    print(f"[{datetime.utcnow()}] {form_data.username} logined")
    return {"access_token": access_token, "token_type": "bearer"} #acces_token must input to header

"""





###--- fast api test pages ---###

@app.get("/j2", response_class=HTMLResponse)
def home(request:Request):  #Request is data type.
    return templets.TemplateResponse("index-1.html", {"request":request})

@app.get("/j", response_class=HTMLResponse)
def home1(request:Request):
    return templets.TemplateResponse("index.html", {"request":request})

@app.get("/h", response_class=HTMLResponse)
def home2(request:Request):
    return templets.TemplateResponse("index-hamin.html", {"request":request})

@app.get("/helloworld", response_class=HTMLResponse)
def helloworld(request:Request):
    return templets.TemplateResponse("helloworld.html", {"request":request})

@app.get("/gettext", response_class=HTMLResponse)
def gettext(request:Request):
    return templets.TemplateResponse("gettext.html", {"request":request,"id":"Made by Fast API"})

#<!------------------------------------->
#This part is examples for get parameter and post parameter.

Flist = ["apple","banana", "orange"]

@app.get("/result")
def result(text: int):
    return Flist[text-1]

"""

class Post(BaseModel):
    text : str

#If input file is form data.
@app.post("/post", response_class=HTMLResponse)
def post(request:Request,text: str=Form(...)):
    return templets.TemplateResponse("post.html", {"request":request, "id":text})

#If input file is json.
@app.post("/post")
def post(post:Post):
    return post


#<!------------------------------------->



"""

#404page 
@app.get("/{item_id}", response_class=HTMLResponse)
def error(request:Request):
    return templets.TemplateResponse("404Page.html", {"request":request})






