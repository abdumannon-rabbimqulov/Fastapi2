from fastapi import FastAPI
from users.models import User
from db import engine, Base
from users.router import router as user_router

app=FastAPI()
app.include_router(user_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

