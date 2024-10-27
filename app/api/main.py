from fastapi import APIRouter
from app.api.routes import ellipticCurve, prime
from app.api.routes.cryptoSystem.main import router as cryptoSytemRouter
from app.api.routes.signatureScheme.main import router as signatureSchemeRouter

router = APIRouter()


@router.get("/api/healthchecker", tags=["Health"])
def healthChecker():
    return {"message": "The API is LIVE!!"}


router.include_router(
    prime.router,
    prefix="/prime",
    tags=["Prime"],
)

router.include_router(
    cryptoSytemRouter,
    prefix="/crypto_system",
    tags=["Crypto System"],
)

router.include_router(
    signatureSchemeRouter,
    prefix="/signature_scheme",
    tags=["Signature Scheme"],
)

router.include_router(
    ellipticCurve.router,
    prefix="/elliptice_curve",
    tags=["Elliptic Curve"],
)
