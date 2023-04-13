from fastapi import FastAPI, Request, APIRouter, Form, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import sys
import json
import logging
import random
# import schemas, database, models
from typing import Iterator
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
router = APIRouter(
    tags=['P3_Web_Pages']
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



################################################################
# -----                     login                        ----- #
################################################################

@router.get("/", response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("login_CovidWatch.html", {"request":request})    #NHRI_Web.html 因Demo暫時修改為 NHRI_Web_demo.html //論文圖修改

################################################################
# -----                    into_P3                       ----- #
################################################################

@router.post("/into_P3", response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("WashHand_Home.html", {"request":request})

################################################################
# -----              Manager_CMS                  ----- #
################################################################


@router.post("/SelectPage", response_class=HTMLResponse)
def register(request: Request,account :str = Form(...), password :str = Form(...)):
    print(f'[DEBUG] inbound request: account: {account}; passowrd: {password}')
    if account == "test" and password == "admin":


        #return templates.TemplateResponse("SelectPage.html", {"request": request,"tests": diclist})
        return templates.TemplateResponse("CovidWatch_Monitor.html", {"request": request})
    else:
        return templates.TemplateResponse("login_P3.html", {"request": request})