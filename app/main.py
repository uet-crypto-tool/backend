from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import router
import uvicorn
import sys

sys.setrecursionlimit(10**6)
sys.set_int_max_str_digits(0)


app = FastAPI(
    title="Uet CryptoTool",
    summary="CryptoTool",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
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
