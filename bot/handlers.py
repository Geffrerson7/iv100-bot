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


token = config.token
is_start_active = False


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_start_active

    if not is_start_active:
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
    else:
        await update.message.reply_text(
            "Las coordenadas ya se están enviando. Si deseas detener el envío de coordenadas, usa /stop"
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global is_start_active

    if not is_start_active:
        total_text = send_pokemon_data()
        if total_text:
            for text in total_text:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=text
                )
                await asyncio.sleep(1)  # Espera 1 segundo entre cada mensaje
            is_start_active = True
        else:
            await update.message.reply_text(
                f"{update.effective_user.first_name} espera unos segundos mientras encontramos pokemons"
            )
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


def send_pokemon_data_to_telegram():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.ERROR,
    )

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("iv100", start))
    application.add_handler(CommandHandler("hello", hello))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
