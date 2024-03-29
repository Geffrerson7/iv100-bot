from settings import config
from api import app
import uvicorn
from telegram import Update
from bot.ptb import ptb
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
)
from bot.handlers import error_handler, text_handler
from bot.commands import start_iv_100, start_iv_90, stop


def add_handlers(dp):
    dp.add_error_handler(error_handler)
    dp.add_handler(CommandHandler("iv100", start_iv_100))
    dp.add_handler(CommandHandler("iv90", start_iv_90))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))


add_handlers(ptb)


if __name__ == "__main__":
    if config.DEBUG == "True":
        ptb.run_polling(allowed_updates=Update.ALL_TYPES)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
