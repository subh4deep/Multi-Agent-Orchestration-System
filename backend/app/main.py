
from fastapi import FastAPI
from backend.app.api.routes import router

app = FastAPI(
    title="DevFlow AI",
    description="AI-powered GitHub issue resolution system",
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Welcome to DevFlow AI"}
