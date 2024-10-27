from __future__ import annotations
import app.core.ellipticCurve.point as point


class Curve(object):
    def __init__(self, a: int, b: int, field: SubGroup, name="undefined"):
        self.name = name
        self.a = a
        self.b = b
        self.field = field
        self.g = point.Point(self, self.field.g[0], self.field.g[1])

    def is_singular(self) -> bool:
        return (4 * self.a**3 + 27 * self.b**2) % self.field.p == 0

    def on_curve(self, x, y) -> bool:
        return (y**2 - x**3 - self.a * x - self.b) % self.field.p == 0

    def __eq__(self, other) -> bool:
        if not isinstance(other, Curve):
            return False
        return self.a == other.a and self.b == other.b and self.field == other.field

    def __ne__(self, other) -> point.Point:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return '"%s" => y^2 = x^3 + %dx + %d (mod %d)' % (
            self.name,
            self.a,
            self.b,
            self.field.p,
        )

    def __repr__(self) -> str:
        return self.__str__()


class SubGroup(object):
    def __init__(self, p: int, g: point.Point, n: int, h: int):
        self.p = p
        self.g = g
        self.n = n
        self.h = h

    def __eq__(self, other: SubGroup) -> bool:
        if not isinstance(other, SubGroup):
            return False
        return (
            self.p == other.p
            and self.g == other.g
            and self.n == other.n
            and self.h == other.h
        )

    def __ne__(self, other: SubGroup) -> SubGroup:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return (
            "Subgroup => generator %s, order: %d, cofactor: %d on Field => prime %d"
            % (self.g, self.n, self.h, self.p)
        )

    def __repr__(self) -> str:
        return self.__str__()
