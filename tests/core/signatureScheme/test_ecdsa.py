from app.core.signatureScheme import ecdsa
import secrets
import random
from app.core.ellipticCurve.domain import CurveDomainParamter


def test_core_signatureScheme_rsa():
    curve_name = random.choice(CurveDomainParamter.list())
    curve_name, d, Q = ecdsa.generateKey(curve_name)
    message = "HelloWorld"
    signature = ecdsa.sign(curve_name, d, message)
    is_valid = ecdsa.verify(curve_name, Q, message, signature)
    assert is_valid == True
