from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware


import LC_Stats
import Roadmap

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],            
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"]              
)

@app.get("/")
def greet():
    return 'Hello Welcome!'

@app.get("/stats/{lc_id}")
def stats_getter(lc_id):
    return LC_Stats.main(lc_id)

@app.get("/roadmap/{data}",response_class=HTMLResponse)
def roadmap_getter(data):
    html = Roadmap.generate(data)
    return HTMLResponse(content=html)
