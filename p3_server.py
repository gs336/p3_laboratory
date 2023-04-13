#from curses.ascii import HT

from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn
from camera_single import Camera
import random
from fastapi.staticfiles import StaticFiles
from routers import P3_router
import os
import asyncio
from datetime import datetime

app = FastAPI()
router = APIRouter()

templates = Jinja2Templates(directory ="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

camera = Camera()

#colors = [tuple([random.randint(0, 255) for _ in range(3)]) for _ in range(100)] #for bbox plotting

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
   return templates.TemplateResponse('login_P3.html', {"request": request})

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        #frame1 = frame[100:200, 0:400]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

async def get_time():
    global camera
    while True:
        now = datetime.now()
        if camera.shooted_num == 1:
            yield f'data: {now.strftime("%H:%M:%S")} 請轉身，將拍攝背面照片\n\n'
            await asyncio.sleep(1)
        elif camera.shooted_num == 2 and not camera.is_detected:
            yield f'data: {now.strftime("%H:%M:%S")} 檢測中，請稍後...\n\n'
            await asyncio.sleep(1)
        elif camera.is_detected:
            yield f'data: {now.strftime("%H:%M:%S")} : <br>{camera.detected_result}\n\n'
            await asyncio.sleep(1)
        else:
            yield f'data: {now.strftime("%H:%M:%S")}: 偵測目標中...\n\n'
            await asyncio.sleep(1)

@app.get('/video_feed', response_class=HTMLResponse)
async def video_feed():
    global camera
    """Video streaming route. Put this in the src attribute of an img tag."""
    return  StreamingResponse(gen(camera),
                    media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/update")
async def clock():
    return StreamingResponse(get_time(),  media_type="text/event-stream")

if not os.path.exists('../photograph'):
    os.makedirs('../photograph')
app.mount("/photograph", StaticFiles(directory="../photograph"), name="photograph")

if __name__ == '__main__':
    import uvicorn
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default = 'localhost')
    parser.add_argument('--port', default = 8000)
    parser.add_argument('--precache-models', action='store_true', 
            help='Pre-cache all models in memory upon initialization, otherwise dynamically caches models')
    opt = parser.parse_args()

   # if opt.precache_models:
    #    model_dict = {model_name: torch.hub.load('ultralytics/yolov5', model_name, pretrained=True) 
    #                   for model_name in model_selection_options}
    
    app_str = 'p3_server:app' #make the app string equal to whatever the name of this file is
    uvicorn.run(app_str, host= opt.host, port=opt.port, reload=True)
