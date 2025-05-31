from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from src.controller.web_controlador import web_router

import uvicorn

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(web_router)

app.mount("/", StaticFiles(directory="src/view/web", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("app_web:app", host="127.0.0.1", port=8000, reload=True)
