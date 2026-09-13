from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.properties import router as properties_router
from app.api.search import router as search_router
from app.api.analysis import router as analysis_router

from app.api.chat import (
    router as chat_router,
)

app = FastAPI(
    title="Real Estate Intelligence API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(
    properties_router,
)

app.include_router(
    search_router,
)

app.include_router(
    chat_router,
)

app.include_router(
    analysis_router,
)
