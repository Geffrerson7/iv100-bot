from contextlib import asynccontextmanager
from fastapi import FastAPI
from settings import config
from telegram.ext import Application
import traceback

ptb = (
    Application.builder()
    .token(config.TOKEN)
    .read_timeout(7)
    .get_updates_read_timeout(42)
    .build()  
)

@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        if config.BOTHOST:
            print(f"Attempting to configure webhook with URL: {config.BOTHOST}")
            webhook_info = await ptb.bot.get_webhook_info()
            if webhook_info.url != config.BOTHOST:
                await ptb.bot.setWebhook(config.BOTHOST)
                print(f"Webhook configured at {config.BOTHOST}")
            else:
                print("Webhook already configured")
        async with ptb:
            await ptb.start()
            yield
    except Exception as e:
        print(f"An error occurred during the lifespan management: {e}")
        traceback.print_exc()
    finally:
        await ptb.stop()