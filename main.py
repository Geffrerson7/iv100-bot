# from bot.handlers import run_bot


# def main():
#     run_bot()


# if __name__ == "__main__":
#     main()
from bot.handlers import setup_handlers
from telegram.ext import Application  # Suponiendo que tengas un módulo application.py donde defines la configuración de tu aplicación
from telegram import Update
import traceback
import logging
from data import config

token = config.token

def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.ERROR,
    )

    application = Application.builder().token(token).build()
    setup_handlers(application)  # Configura los manejadores de eventos en la aplicación
    try:
        print("El Bot de Telegram ahora se ejecutará en modo de run_polling.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logging.error("An error occurred during polling: {e}", exc_info=True)
        traceback.print_exc()

if __name__ == "__main__":
    main()
