from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from telegram import ReplyKeyboardMarkup
from data import config
import traceback
import html
import json
from telegram.constants import ParseMode
from common.log import logger
from common.constans import is_start_active

DEVELOPER_CHAT_ID = config.DEVELOPER_CHAT_ID

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_start_active
    # Verificar si ya hay una instancia activa del bot
    if is_start_active:
        await update.message.reply_text(
            "Lo siento, ya hay una instancia activa del bot. Por favor, espera a que se detenga antes de iniciar otra."
        )
        return

    # Si no hay instancia activa, proceder con el manejo del mensaje
    user_name = update.effective_user.first_name
    message_text = f"¡Hola {user_name}, bienvenido a Adventure Elements!\n"
    message_text += "Este es un menú explicativo:\n\n"
    message_text += "/iv100 - Inicia el bot.\n"
    message_text += "/stop - Detiene el bot.\n"

    keyboard = [["/iv100", "/stop"]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )

    await update.message.reply_text(message_text, reply_markup=reply_markup)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""

    logger.error("Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )


