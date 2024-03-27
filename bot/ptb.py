from contextlib import asynccontextmanager
from fastapi import FastAPI
from settings import config
from telegram.ext import Application


ptb = (
    Application.builder()
    .token(config.TOKEN)
    .read_timeout(7)
    .get_updates_read_timeout(42)
)
if config.DEBUG == "True":
    ptb = ptb.build()
else:
    ptb = ptb.updater(None).build()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if config.BOTHOST:
        webhook_info = await ptb.bot.get_webhook_info()
        if webhook_info.url != config.BOTHOST:
            await ptb.bot.setWebhook(config.BOTHOST)
            print(f"Webhook configured at {config.BOTHOST}")
        else:
            print("Webhook already configured")
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()