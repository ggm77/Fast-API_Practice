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
from enum import Enum
from typing import Any

#app = FastAPI(docs_url="/documentation", redoc_url=None) #Build app and remove documentation page.
app = FastAPI()

templets = Jinja2Templates(directory="templates") # html

app.mount("/static", StaticFiles(directory="static"), name="static") # css and js

@app.get("/", response_class=HTMLResponse)
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
    return templets.TemplateResponse("gettext.html", {"request":request})




##########


list = ["apple","banana", "orange"]

@app.get("/result")
def result(text: int):
    return list[text-1]


class Post(BaseModel):
    text : str

"""
@app.post("/post")
def post(text: str=Form(...)):
    return text
"""

@app.post("/post")
def post(post:Post):
    return post


#############




@app.get("/{item_id}", response_class=HTMLResponse)
def error(request:Request):
    return templets.TemplateResponse("404Page.html", {"request":request})






