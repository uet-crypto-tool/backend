import sys
from generators import GeneratePrimeUseAPI
from rsa import RSA
from elgamal import ElGamal
from ecc import ECC
from ellipticCurve import get_curve, Curve, Point
from ecdsa import ECDSA
from utils import encodeString
import unittest

sys.set_int_max_str_digits(0)

# print("====== Setup ======")
# p = GeneratePrimeUseAPI(8192)
# q = GeneratePrimeUseAPI(8192)
# m = 9726

# print("p: {}".format(p))
# print("q: {}".format(q))
# print("message m: {}".format(m))

# print("==== RSA =====")
# rsa = RSA(p=p, q=q)
# print("PublicKey: {}".format(rsa.getPublicKey()))
# signed = rsa.sign(m)
# print("signed: {}".format(signed))
# verify = rsa.verify(m, signed)
# print("verify: {}".format(verify))

# print("======= ELGAMAL ======")
# elgamal = ElGamal(p=p, a=765)

# print("PublicKey: {}".format(elgamal.getPublicKey()))

# y1, y2 = elgamal.sign(m)
# print("y1: {}".format(y1))
# print("y2: {}".format(y2))

# verify = elgamal.verify(m, y1, y2)
# print("verify: {}".format(verify))

# print("======= ECC ======")
# curve = get_curve('secp521r1')
# P = Point(curve, 0x000000c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66,
#           0x0000011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650)
# ecc = ECC(curve, P)
# print(ecc)

# m1, m2 = ecc.encrypt(P)
# print(P == ecc.decrypt(m1, m2))

# print("======== ECDSA ====== ")
# curve = get_curve("secp521r1")
# P = Point(
#     curve,
#     0x000000C6858E06B70404E9CD9E3ECB662395B4429C648139053FB521F828AF606B4D3DBAA14B5E77EFE75928FE1DC127A2FFA8DE3348B3C1856A429BF97E7E31C2E5BD66,
#     0x0000011839296A789A3BC0045C8A5FB42C7D1BD998F54449579B446817AFBD17273E662C97EE72995EF42640C550B9013FAD0761353C7086A272C24088BE94769FD16650,
# )
# ecdsa = ECDSA(curve, P)
# print("PublicKey: {}".format(ecdsa.getPublicKey()))

# m = encodeString("PHUONG")
# r, s = ecdsa.sign(m)
# print("r: {}".format(r))
# print("s: {}".format(s))

# verify = ecdsa.verify(m, r, s)
# print("verify: {}", verify)
