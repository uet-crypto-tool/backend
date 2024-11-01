from app.core.ellipticCurve import Koblitz
import random
from app.core.ellipticCurve.domain import CurveDomainParamter
from app.core.cryptoSystem import ecc


def test_pipline():
    message = "Hello, Elliptic Curve Cryptography! " * 10
    curve_name = random.choice(CurveDomainParamter.list())
    encoded_points, scale_factor = Koblitz.encode(
        message=message, curve_name=curve_name)
    decoded_message = Koblitz.decode(encoded_points, scale_factor)
    assert decoded_message == message


def test_ecc_with_kiblitz():
    message = "Hello, Elliptic Curve Cryptography! " * 10
    curve_name = random.choice(CurveDomainParamter.list())
    curve = CurveDomainParamter.get(curve_name)
    privateKey, publicKey = ecc.generateKey(curve)
    encrypted_pairs = ecc.encryptPlainText(publicKey, message)
    decrypted = ecc.decryptPlainText(privateKey, encrypted_pairs)
    assert decrypted == message
