import asyncio
from bot.service import send_pokemon_data
from telegram import Update
from telegram.ext import ContextTypes

is_start_active = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global is_start_active

    if not is_start_active:
        try:
            is_start_active = True  
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


async def stop(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    global is_start_active
    if is_start_active:
        is_start_active = False
    else:
        await update.message.reply_text("El envío de coordenadas ha sido detenido.")