"""
Date : 2023.04.28
Author : 서하민

FastApi practice app


"""

# run web page ->  uvicorn main:app --reload        ## main->file name  // app->app name


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(docs_url="/documentation", redoc_url=None) #Build app and remove documentation page.

templets = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

num = 1

@app.get("/", response_class=HTMLResponse)
def home(request:Request):  #Request is data type.
    return templets.TemplateResponse("index.html", {"request":request})




