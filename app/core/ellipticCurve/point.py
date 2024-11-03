from __future__ import annotations
import app.core.ellipticCurve.curve as curve
from pydantic import BaseModel
import warnings
from app.core.utils import inverse_mod

# Python3 compatibility
try:
    LONG_TYPE = long
except NameError:
    LONG_TYPE = int


class PointType(BaseModel):
    x: int
    y: int


class Point(object):
    def __init__(self, curve: curve.Curve, x: int, y: int):
        self.curve = curve
        self.x = x
        self.y = y
        self.p = self.curve.p
        self.on_curve = self.curve.on_curve(self.x, self.y)
        if not self.on_curve:
            warnings.warn(
                'Point (%d, %d) is not on curve "%s"' % (self.x, self.y, self.curve)
            )

    def __m(self, p, q):
        if p.x == q.x:
            return (3 * p.x**2 + self.curve.a) * inverse_mod(2 * p.y, self.p)
        else:
            return (p.y - q.y) * inverse_mod(p.x - q.x, self.p)

    def __eq__(self, other: Point) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y and self.curve == other.curve

    def __ne__(self, other: Point) -> bool:
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, Inf):
            return self
        if isinstance(other, Point):
            if self.x == other.x and self.y != other.y:
                return Inf(self.curve)
            elif self.curve == other.curve:
                m = self.__m(self, other)
                x_r = (m**2 - self.x - other.x) % self.p
                y_r = -(self.y + m * (x_r - self.x)) % self.p
                return Point(self.curve, x_r, y_r)
            else:
                raise ValueError("Cannot add points belonging to different curves")
        else:
            raise TypeError(
                "Unsupported operand type(s) for +: '%s' and '%s'"
                % (other.__class__.__name__, self.__class__.__name__)
            )

    def __sub__(self, other):
        if isinstance(other, Inf):
            return self.__add__(other)
        if isinstance(other, Point):
            return self.__add__(Point(self.curve, other.x, -other.y % self.p))
        else:
            raise TypeError(
                "Unsupported operand type(s) for -: '%s' and '%s'"
                % (other.__class__.__name__, self.__class__.__name__)
            )

    def __mul__(self, other):
        if isinstance(other, Inf):
            return Inf(self.curve)
        if isinstance(other, int) or isinstance(other, LONG_TYPE):
            if other % self.curve.n == 0:
                return Inf(self.curve)
            if other < 0:
                addend = Point(self.curve, self.x, -self.y % self.p)
            else:
                addend = self
            result = Inf(self.curve)
            # Iterate over all bits starting by the LSB
            for bit in reversed([int(i) for i in bin(abs(other))[2:]]):
                if bit == 1:
                    result += addend
                addend += addend
            return result
        else:
            raise TypeError(
                "Unsupported operand type(s) for *: '%s' and '%s'"
                % (other.__class__.__name__, self.__class__.__name__)
            )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self) -> str:
        return "(%d, %d) %s %s" % (
            self.x,
            self.y,
            "on" if self.on_curve else "off",
            self.curve,
        )

    def __repr__(self) -> str:
        return self.__str__()

    def type(self):
        return PointType(x=self.x, y=self.y)


class Inf(object):
    def __init__(self, curve: curve.Curve, x: int = None, y: int = None):
        self.x = x
        self.y = y
        self.curve = curve

    def __eq__(self, other):
        if not isinstance(other, Inf):
            return False
        return self.curve == other.curve

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, Inf):
            return Inf()
        if isinstance(other, Point):
            return other
        raise TypeError(
            "Unsupported operand type(s) for +: '%s' and '%s'"
            % (other.__class__.__name__, self.__class__.__name__)
        )

    def __sub__(self, other):
        if isinstance(other, Inf):
            return Inf()
        if isinstance(other, Point):
            return other
        raise TypeError(
            "Unsupported operand type(s) for +: '%s' and '%s'"
            % (other.__class__.__name__, self.__class__.__name__)
        )

    def __str__(self) -> str:
        return "%s on %s" % (self.__class__.__name__, self.curve)

    def __repr__(self) -> str:
        return self.__str__()
