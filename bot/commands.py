import asyncio
from bot.service import generate_pokemon_messages
from telegram import Update
from telegram.ext import ContextTypes
from data import config
import telegram

# ID del grupo al que se enviarán las coordenadas
GRUPO_COORDENADAS_ID = int(config.CHAT_ID)

# Lista de usuarios permitidos para activar los comandos
USUARIOS_PERMITIDOS = [int(config.SUPPORT), int(config.ADMIN)]

PERIOD = int(config.PERIOD)


async def callback_coordinate(context: ContextTypes.DEFAULT_TYPE):
    try:
        total_text = generate_pokemon_messages()

        if total_text:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID, text="Enviando coordenadas..."
            )
            for text in total_text:
                await context.bot.send_message(
                    chat_id=GRUPO_COORDENADAS_ID, text=text, parse_mode="MarkdownV2"
                )
                await asyncio.sleep(2)
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                text=f"Se terminó de enviar las coordenadas. Dentro de {PERIOD} minutos se enviarán más.",
            )

    except telegram.error.RetryAfter as e:
        await asyncio.sleep(e.retry_after)
        message = (
            f"Se pausó temporalmente el envío de coordenadas debido a un límite de velocidad. "
            f"Se reanudará automáticamente en {e.retry_after} segundos."
        )
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            text=message,
        )
        print(f"Error de RetryAfter en callback_coordinate: {e}")
        total_text = generate_pokemon_messages()
        for text in total_text:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID, text=text, parse_mode="MarkdownV2"
            )
            await asyncio.sleep(2)
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            text=f"Se terminó de enviar las coordenadas. Dentro de {PERIOD} minutos se enviarán más.",
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Verificar si el usuario está permitido para activar los comandos
        if update.effective_user.id not in USUARIOS_PERMITIDOS:
            await update.message.reply_text(
                "No tienes permiso para activar los comandos."
            )
            return

        # Verificar si el mensaje proviene del grupo de coordenadas
        if update.effective_chat.id != GRUPO_COORDENADAS_ID:
            await update.message.reply_text(
                "Los comandos solo pueden ser activados en el grupo de @top100galaxy1"
            )
            return
        job = context.chat_data.get("callback_coordinate")

        if job:
            await update.message.reply_text(
                "Las coordenadas ya se están enviando. Si desea detener el envío digite /stop"
            )
        else:
            await update.message.reply_text(
                "En 10 segundos se enviarán las coordenadas..."
            )
            job = context.job_queue.run_repeating(
                callback_coordinate, interval=PERIOD * 60, first=10
            )
            context.chat_data["callback_coordinate"] = job

    except telegram.error.TelegramError as e:
        print(f"Error de Telegram: {e}")
        await update.message.reply_text(
            "Se ha producido un error al ejecutar el comando /iv100. Por favor, inténtalo de nuevo más tarde."
        )

    except Exception as e:
        print(f"Error en start: {e}") 
        await update.message.reply_text(
            "Se ha producido un error. Por favor, inténtalo de nuevo más tarde."
        )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Verificar si el usuario está permitido para usar el comando
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        await update.message.reply_text(
            "No tienes permiso para detener el envío de coordenadas."
        )
        return

    # Verificar si el mensaje proviene del grupo de coordenadas
    if update.effective_chat.id != GRUPO_COORDENADAS_ID:
        await update.message.reply_text(
            "Los comandos solo pueden ser activados en el grupo de @top100galaxy1"
        )
        return

    job = context.chat_data.get("callback_coordinate")

    if job:
        job.schedule_removal()
        del context.chat_data["callback_coordinate"]
        await update.message.reply_text("El envío de coordenadas ha sido detenido.")
    else:
        await update.message.reply_text(
            "Ya dejé de enviar coordenadas. Si quieres que siga enviando usa /iv100"
        )
