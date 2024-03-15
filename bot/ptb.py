from contextlib import asynccontextmanager
from fastapi import FastAPI
from data import config
from telegram.ext import Application


ptb = (
    Application.builder()
    .token(config.TOKEN)
    .read_timeout(7)
    .get_updates_read_timeout(42)
)
if config.DEBUG:
    ptb = ptb.build()
else:
    ptb = ptb.updater(None)


@asynccontextmanager
async def lifespan(_: FastAPI):
    if config.BOTHOST:
        await ptb.bot.setWebhook(config.BOTHOST)
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()
