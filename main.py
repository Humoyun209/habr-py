from typing import Annotated
from fastapi import Cookie, Depends, FastAPI, HTTPException, Header, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from app.users.router import router as user_router

app = FastAPI()

app.include_router(user_router)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_home():
    return {'Message': 'Welcome to Full Stack'}
