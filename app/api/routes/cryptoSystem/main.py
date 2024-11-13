from fastapi import APIRouter
from app.api.routes.cryptoSystem.symmetric.main import router as SymmetricRouter
from app.api.routes.cryptoSystem.asymmetric.main import router as AsymmetricRouter

router = APIRouter()

router.include_router(
    SymmetricRouter, prefix="/symmetric", tags=["Symmetric CryptoSystem"]
)
router.include_router(
    AsymmetricRouter, prefix="/asymmetric", tags=["Asymmetric CryptoSystem"]
)
