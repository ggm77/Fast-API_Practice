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


from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json


#app = FastAPI(docs_url="/documentation", redoc_url=None) #Build app and remove documentation page.
app = FastAPI()

templets = Jinja2Templates(directory="templates") # html

app.mount("/static", StaticFiles(directory="static"), name="static") # css and js

@app.get("/", response_class=HTMLResponse)
def first(request:Request):
    return templets.TemplateResponse("home.html", {"request":request})

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


class Post(BaseModel):
    text : str

#If input file is form data.
@app.post("/post", response_class=HTMLResponse)
def post(request:Request,text: str=Form(...)):
    return templets.TemplateResponse("post.html", {"request":request, "id":text})
"""
#If input file is json.
@app.post("/post")
def post(post:Post):
    return post
"""

#<!------------------------------------->


@app.get("/login", response_class=HTMLResponse)
def login(request:Request):
    return templets.TemplateResponse("login.html", {"request":request})

data = {"ggm":"1234","hhm":"2345"}
dict = {"ggm":{"id":"ggm", "level":15, "skill":["Python","C","Java","HTML","CSS","JavaScript","React-native","Fast API"]}, "hhm":{"id":"hhm","level":10,"skill":["Python","C","Java"]}}

class userInfo(BaseModel):
    id: str
    level: int
    skill: list

@app.post("/myprofile", response_class=HTMLResponse, response_model=userInfo)
def myprofile(request:Request, id: str=Form(...), password: str=Form(...)):
    if (id in data and data[id]==password):
        print(f"{id} login sucsess")

        userData = json.dumps(dict[id]) # dict to json

        return templets.TemplateResponse("myprofile.html", {"request":request, "id":id, "data":userData}) # userData is json file.
    else:
        print(f"{id} login fail")
        return templets.TemplateResponse("loginError.html", {"request":request})




#404page 
@app.get("/{item_id}", response_class=HTMLResponse)
def error(request:Request):
    return templets.TemplateResponse("404Page.html", {"request":request})






