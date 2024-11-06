from app.core.cryptoSystem import ecc
import secrets
import random
from app.core.ellipticCurve.domain import CurveDomainParamter


def test_core_cryptoSystem_ecc():
    secret_number = secrets.randbits(100)
    curve_name = random.choice(CurveDomainParamter.list())
    curve_name, secret_number, B = ecc.generateKey(curve_name, secret_number)

    message = str(secrets.randbits(8))
    encrypted_message = ecc.encrypt(curve_name, B, message)
    decrypted_message = ecc.decrypt(curve_name, secret_number, encrypted_message)
    assert decrypted_message == message
