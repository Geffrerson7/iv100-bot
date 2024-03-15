from telegram import Update
from telegram.ext import (
    CommandHandler,
    Application,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram import ReplyKeyboardMarkup
import logging, asyncio
from bot.service import send_pokemon_data
from data import config
import traceback
import html
import json
from telegram.constants import ParseMode

token = config.token
DEVELOPER_CHAT_ID = config.developer_chat_id
is_start_active = False
logger = logging.getLogger(__name__)


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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global is_start_active

    if not is_start_active:
        try:
            is_start_active = True  # Marcamos que la tarea está activa
            total_text = send_pokemon_data()

            if total_text:
                for text in total_text:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id, text=text
                    )
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"Error en send_pokemon_data(): {e}")  # Imprime el error
            await update.message.reply_text(
                "Ocurrió un error al obtener los datos de los Pokémon. Por favor, inténtalo de nuevo más tarde."
            )
        finally:
            is_start_active = False  # Marcamos que la tarea ha terminado
    else:
        await update.message.reply_text(
            "Las coordenadas ya se están enviando. Si deseas detener el envío de coordenadas, usa /stop"
        )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global is_start_active
    if is_start_active:
        is_start_active = False
        await update.message.reply_text("El envío de coordenadas ha sido detenido.")
    else:
        await update.message.reply_text("El envío de coordenadas no está activa.")


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


def run_bot():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.ERROR,
    )

    application = Application.builder().token(token).build()

    application.add_error_handler(error_handler)

    application.add_handler(CommandHandler("iv100", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler)
    )

    try:
        print("El Bot de Telegram ahora se ejecutará en modo de run_polling.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logging.error("An error occurred during polling: {e}", exc_info=True)
        traceback.print_exc()
