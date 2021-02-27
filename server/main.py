from typing import Optional

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

# model
from engine import Searcher
searcher = Searcher()

app = FastAPI()

# need to take care of CORS
# because we call from youtube.com to localhost:8000
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://youtube.com"
    "https://youtube.com",
    "http://www.youtube.com",
    "https://www.youtube.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/searcher")
def read_root(
    url: str = "https://www.youtube.com/watch?v=bfHEnw6Rm-4",
    query: str = 'qd cre',
    limit = 5,
    languages = ['en'],
    mode = 'FUZZY'
    ):

    res = searcher.main(url, query=query, limit=limit, languages=languages, mode=mode)
    return {
        "result": res
    }
