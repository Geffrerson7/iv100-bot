from data import config
from fastapi import FastAPI
from bot.ptb import lifespan


app = FastAPI(lifespan=lifespan) if config.DEBUG else FastAPI()


@app.get("/")
def home():
    return "Hello world!"

