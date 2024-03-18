import asyncio
from bot.service import send_pokemon_data
from telegram import Update
from telegram.ext import ContextTypes
from common.constans import is_start_active


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global is_start_active

    if not is_start_active:
        try:
            is_start_active = True  
            total_text = send_pokemon_data()

            if total_text:
                for text in total_text:
                    if not is_start_active:
                        break
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id, text=text
                    )
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"Error en send_pokemon_data(): {e}") 
            await update.message.reply_text(
                "Ocurrió un error al obtener los datos de los Pokémon. Por favor, inténtalo de nuevo más tarde."
            )

async def stop(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    global is_start_active

    if is_start_active:
        is_start_active = False
        await update.message.reply_text("El envío de coordenadas ha sido detenido.")
    else:
        await update.message.reply_text("El envío de coordenadas no está activo.")

