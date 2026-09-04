from fastapi import FastAPI
from app.config import settings
from app.routes import router


app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
