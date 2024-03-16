from data import config
from fastapi import FastAPI
from bot.ptb import lifespan


app =  FastAPI() if config.DEBUG else FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return "Hello world!"

