from app.core.ellipticCurve.domain import CurveDomainParamter
from app.core.ellipticCurve.point import Point
from app.core.utils import inverse_mod, mul_mod
from app.core.generators import randomIntInRange
from app.schemas.ecdsa_schemas import Seed, PrivateKey, PublicKey, Signature


def generateKey(curve_name: str):
    curve = CurveDomainParamter.get(curve_name)
    d = randomIntInRange(1, curve.n - 1)
    Q = curve.g * d
    return (
        PrivateKey(curve_name=curve_name, d=d),
        PublicKey(curve_name=curve_name, Q=Q.type()),
    )


def H(x: int) -> int:
    return x


def sign(privateKey: PrivateKey, message: int) -> Signature:
    curve = CurveDomainParamter.get(privateKey.curve_name)
    G = curve.g
    n = curve.n
    r = 0
    s = 0
    while s == 0:
        k = 1
        while r == 0:
            k = randomIntInRange(1, n - 1)
            x = (G * k).x
            r = x % n

        h = H(message)
        dr_mod_n = mul_mod(privateKey.d, r, n)
        h_plus_dr_mod_n = (h + dr_mod_n) % (n)
        k_inv = inverse_mod(k, n)
        s = mul_mod(h_plus_dr_mod_n, k_inv, n)

    return Signature(r=r, s=s)


def verify(publicKey: PublicKey, message: int, signature: Signature) -> bool:
    curve = CurveDomainParamter.get(publicKey.curve_name)
    G = curve.g
    Q = Point(curve, publicKey.Q.x, publicKey.Q.y)
    r, s = signature.r, signature.s

    n = curve.n
    w = inverse_mod(s, n)
    h = H(message)
    u1 = mul_mod(h, w, n)
    u2 = mul_mod(r, w, n)
    x = (G * u1 + Q * u2).x
    v = x % n

    return v == r
