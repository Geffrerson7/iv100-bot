import asyncio
from bot.service import send_pokemon_data
from telegram import Update
from telegram.ext import ContextTypes
from common.constans import is_start_active
from data import config


# ID del grupo al que se enviarán las coordenadas
GRUPO_COORDENADAS_ID = int(config.CHAT_ID)

# Lista de usuarios permitidos para activar los comandos
USUARIOS_PERMITIDOS = [int(config.SUPPORT), int(config.ADMIN)] 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global is_start_active

    # Verificar si el usuario está permitido para activar los comandos
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        await update.message.reply_text("No tienes permiso para activar los comandos.")
        return

    # Verificar si el mensaje proviene del grupo de coordenadas
    if update.effective_chat.id != GRUPO_COORDENADAS_ID:
        await update.message.reply_text("Los comandos solo pueden ser activados en el grupo de @top100galaxy1")
        return

    if not is_start_active:
        try:
            is_start_active = True  
            total_text = send_pokemon_data()

            if total_text:
                for text in total_text:
                    if not is_start_active:
                        break
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,  # Cambiado a enviar al grupo de coordenadas
                        text=text
                    )
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"Error en send_pokemon_data(): {e}") 
            await update.message.reply_text(
                "Ocurrió un error al obtener los datos de los Pokémon. Por favor, inténtalo de nuevo más tarde."
            )

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global is_start_active

    # Verificar si el usuario está permitido para usar el comando
    if update.effective_user.id not in USUARIOS_PERMITIDOS:
        await update.message.reply_text("No tienes permiso para detener el envío de coordenadas.")
        return

    # Verificar si el mensaje proviene del grupo de coordenadas
    if update.effective_chat.id != GRUPO_COORDENADAS_ID:
        await update.message.reply_text("Los comandos solo pueden ser activados en el grupo de @top100galaxy1")
        return

    if is_start_active:
        is_start_active = False
        await update.message.reply_text("El envío de coordenadas ha sido detenido.")
    else:
        await update.message.reply_text("El envío de coordenadas no está activo.")