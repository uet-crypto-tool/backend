from app.core.signatureScheme import elgamal
from app.core.prime.generator import generateProbablePrime
import secrets


def test_core_signatureSheme_rsa():
    p = generateProbablePrime(100)
    a = secrets.randbits(100)

    p, a, alpha, beta = elgamal.generateKey(p, a)
    message = "HelloWorld"
    signature = elgamal.sign(p, a, alpha, message)
    is_valid = elgamal.verify(p, alpha, beta, message, signature)
    assert is_valid == True
