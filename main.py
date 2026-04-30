from fastapi import FastAPI
from users.models import User
from db import engine, Base
from users.router import router as user_router

app=FastAPI()
app.include_router(user_router)


import asyncio

async def startup():
    for _ in range(10):
        try:
            async with engine.begin() as conn:
                print("DB connected ✅")
                return
        except Exception:
            print("DB kutilyapti...")
            await asyncio.sleep(2)
