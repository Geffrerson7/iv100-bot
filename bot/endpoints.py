from fastapi import APIRouter, Request, Response
from telegram import Update
from bot.ptb import ptb
from http import HTTPStatus

router = APIRouter()

@router.get("/")
def home():
    return "Hello world!"

@router.get("/bot")
def bot():
    return "Hello bot!"

@router.post("/")
async def process_update(request: Request):
    req = await request.json()
    update = Update.de_json(req, ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=HTTPStatus.OK)


