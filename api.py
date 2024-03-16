from data import config
from fastapi import FastAPI
from bot.ptb import lifespan
import uvicorn

app =  FastAPI() if config.DEBUG else FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return "Hello world!"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
