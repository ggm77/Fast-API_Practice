"""
Date : 2023.04.28
Author : 서하민

FastApi practice app


"""

# run web page ->  uvicorn main:app --reload        ## main->file name  // app->app name


from fastapi import FastAPI # Import FastAPI.
from fastapi import Request
from fastapi.templating import Jinja2Templates # html display module

templets = Jinja2Templates(directory="templates")


app = FastAPI(docs_url="/documentation", redoc_url=None) #Build app and remove documentation page.

@app.get("/")
def home(request:Request):
    return templets.TemplateResponse("index.html", {"request":request})




