from app.core.ellipticCurve import Koblitz
import random
from app.core.ellipticCurve.domain import CurveDomainParamter


def test_pipline():
    message = "Hello, Elliptic Curve Cryptography! " * 10
    curve_name = random.choice(CurveDomainParamter.list())
    print(f"curve_name: {curve_name}")
    encoded_messages = Koblitz.encode(
        message=message, curve_name=curve_name)
    print(f"encoded_message: {encoded_messages}")

    decoded_message = Koblitz.decode(encoded_messages)
    print(f"decoded_message:{decoded_message}")
    assert decoded_message == message
