from app.core.signatureScheme import rsa
from app.core.generators import generateProbablePrime
import secrets


def test_core_signatureScheme_rsa():
    p = generateProbablePrime(100)
    q = generateProbablePrime(100)

    n, d, e = rsa.generateKey(p, q)
    message = secrets.randbits(8)
    signature = rsa.sign(n, d, message)
    is_valid = rsa.verify(n, e, message, signature)
    assert is_valid == True
