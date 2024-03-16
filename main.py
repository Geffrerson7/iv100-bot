from data import config
from api import app
import uvicorn, logging
from http import HTTPStatus
from telegram import Update
from bot.ptb import ptb
from fastapi import Request, Response
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
)
from bot.handlers import error_handler, text_handler 
from bot.commands import start, stop

def add_handlers(dp):
    dp.add_error_handler(error_handler)
    dp.add_handler(CommandHandler("iv100", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler)
    )

add_handlers(ptb)

if not config.DEBUG:
    @app.post("/")
    async def process_update(request: Request):
        req = await request.json()
        update = Update.de_json(req, ptb.bot)
        await ptb.process_update(update)
        return Response(status_code=HTTPStatus.OK)

if __name__ == "__main__":
    if config.DEBUG:
        logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.ERROR,
    )
        ptb.run_polling(allowed_updates=Update.ALL_TYPES)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)