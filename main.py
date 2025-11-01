from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import LC_Stats
import Roadmap

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vedantsingh-dev.github.io", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def greet():
    return JSONResponse(
        content={"message": "Hello Welcome!"},
        headers={
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff"
        }
    )

@app.get("/stats/{lc_id}")
def stats_getter(lc_id):
    result = LC_Stats.main(lc_id)
    return JSONResponse(
        content=result,
        headers={
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff"
        }
    )

@app.get("/roadmap/{data}", response_class=HTMLResponse)
def roadmap_getter(data):
    html = Roadmap.generate(data)
    return HTMLResponse(
        content=html,
        headers={
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff"
        }
    )
