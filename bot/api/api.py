from fastapi import FastAPI

from bot.api.routers import get


app = FastAPI()

app.include(get.router)