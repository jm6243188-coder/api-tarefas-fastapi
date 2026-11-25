from fastapi import FastAPI
from routes.tarefas import router

app = FastAPI()
app.include_router(router)