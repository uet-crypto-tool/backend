from sage.all import *
from sage.all_cmdline import * 

class EllipticCurve:
    def __init__(p, a, b):
        _const_a = Integer(a)
        _const_b = Integer(b)
        _const_p = Integer(p)
        E = EllipticCurve(GF(_const_p), [_const_a , _const_b])
        return E

    def encrypt(self, public_key, message):
        return 