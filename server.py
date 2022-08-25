#from curses.ascii import HT

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn
from camera_single import Camera
import random, os
from fastapi.staticfiles import StaticFiles



app = FastAPI()
templates = Jinja2Templates(directory = 'templates')

colors = [tuple([random.randint(0, 255) for _ in range(3)]) for _ in range(100)] #for bbox plotting

@app.get("/")
def home(request: Request):
    ''' Returns html jinja2 template render for home page form
    '''

    return templates.TemplateResponse('home.html', {
            "request": request
           
        })


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
   return templates.TemplateResponse('home.html', {"request": request})

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        #frame1 = frame[100:200, 0:400]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get('/video_feed', response_class=HTMLResponse)
async def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return  StreamingResponse(gen(Camera()),
                    media_type='multipart/x-mixed-replace; boundary=frame')

    
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
    
    app_str = 'server:app' #make the app string equal to whatever the name of this file is
    uvicorn.run(app_str, host= opt.host, port=opt.port, reload=True)
