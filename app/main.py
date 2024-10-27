from fastapi import FastAPI
from app.api.main import router
import uvicorn

app = FastAPI(
    title="Uet CryptoTool",
    summary="CryptoTool",
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
