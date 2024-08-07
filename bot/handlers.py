from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from settings.config import (
    CHAT_ID,
    SUPPORT,
    ADMIN,
    PERIOD,
    MESSAGE_THREAD_ID,
    DEVELOPER_CHAT_ID,
)
import traceback
import html
import json
from telegram.constants import ParseMode
from common.log import logger

# ID del grupo al que se enviarán las coordenadas
GRUPO_COORDENADAS_ID = int(CHAT_ID)
# Lista de usuarios permitidos para activar los comandos
USUARIOS_PERMITIDOS = [int(SUPPORT), int(ADMIN)]
# Periodo de tiempo en minutos en el que el bot busca coordenadas
PERIOD = int(PERIOD)
# ID del tema del grupo al que se enviarán las coordenadas
TEMA_ID = int(MESSAGE_THREAD_ID)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message is None:
        return
    # Verificar si el mensaje proviene del grupo permitido
    if update.effective_chat.id != GRUPO_COORDENADAS_ID:
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="Los comandos solo pueden ser activados en el grupo de @top100galaxy1",
        )
        return

    # Verificar si el usuario está permitido para usar el comando
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="No tienes permiso para utilizar este comando.",
        )
        return

    job_iv_90 = context.chat_data.get("callback_coordinate_iv_90")
    job_iv_100 = context.chat_data.get("callback_coordinate_iv_100")

    if job_iv_100 or job_iv_90:
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="Lo siento, ya hay una instancia activa del bot. Por favor, espera a que se detenga antes de iniciar otra.",
        )
        return

    # Si no hay instancia activa, proceder con el manejo del mensaje
    user_name = update.effective_user.first_name
    message_text = f"¡Hola {user_name}, bienvenido a Adventure Elements!\n"
    message_text += "Este es un menú explicativo:\n\n"
    message_text += "/iv100 - Inicia el envío de coordenadas con IV 100.\n"
    message_text += "/iv90 - Inicia el envío de coordenadas con IV 90.\n"
    message_text += "/stop - Detiene el envío de coordenadas.\n"
    await context.bot.send_message(
        chat_id=GRUPO_COORDENADAS_ID,
        message_thread_id=TEMA_ID,
        text=message_text,
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Limitar la longitud del mensaje si es demasiado largo
    max_message_length = 4000

    try:
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

        if len(message) > max_message_length:
            message = (
                message[:max_message_length]
                + " [...Mensaje truncado debido a la longitud...]"
            )

        await context.bot.send_message(
            chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
        )
    except Exception as e:
        print(f"Error en error_handler(): {e}")
