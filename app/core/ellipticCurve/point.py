from __future__ import annotations
import app.core.ellipticCurve.curve as curve
from pydantic import BaseModel
import warnings
from app.core.utils import inverse_mod

# Python3 compatibility
LONG_TYPE = int if "long" not in globals() else "long"


class PointType(BaseModel):
    """
    Represents a point on the elliptic curve, used for serialization.
    """

    x: int
    y: int


class Point:
    """
    Represents a point on an elliptic curve and provides methods for point arithmetic.

    Attributes:
        curve: The elliptic curve this point belongs to.
        x: The x-coordinate of the point.
        y: The y-coordinate of the point.
        p: The prime order of the curve.
        on_curve: A boolean indicating whether the point lies on the curve.
    """

    def __init__(self, curve: curve.Curve, x: int, y: int):
        """
        Initializes a point on the elliptic curve.

        Args:
            curve: The elliptic curve this point belongs to.
            x: The x-coordinate of the point.
            y: The y-coordinate of the point.

        Raises:
            Warning if the point is not on the curve.
        """
        self.curve = curve
        self.x = x
        self.y = y
        self.p = self.curve.p
        self.on_curve = self.curve.on_curve(self.x, self.y)
        if not self.on_curve:
            warnings.warn(f'Point ({self.x}, {self.y}) is not on curve "{self.curve}"')

    def __m(self, p, q):
        """
        Computes the slope (m) for elliptic curve point addition.

        Args:
            p: The first point.
            q: The second point.

        Returns:
            The slope value (m) for point addition.
        """
        if p.x == q.x:
            return (3 * p.x**2 + self.curve.a) * inverse_mod(2 * p.y, self.p)
        return (p.y - q.y) * inverse_mod(p.x - q.x, self.p)

    def __eq__(self, other: Point) -> bool:
        """
        Checks equality between two points on the same curve.

        Args:
            other: The point to compare against.

        Returns:
            True if the points are equal, False otherwise.
        """
        return (
            isinstance(other, Point)
            and self.x == other.x
            and self.y == other.y
            and self.curve == other.curve
        )

    def __ne__(self, other: Point) -> bool:
        """
        Checks inequality between two points.

        Args:
            other: The point to compare against.

        Returns:
            True if the points are not equal, False otherwise.
        """
        return not self.__eq__(other)

    def __add__(self, other):
        """
        Adds this point to another point or to the point at infinity.

        Args:
            other: The point to add.

        Returns:
            The result of adding the two points.

        Raises:
            ValueError if the points belong to different curves.
            TypeError if the operand is not a Point or Inf.
        """
        if isinstance(other, Inf):
            return self
        if isinstance(other, Point):
            if self.x == other.x and self.y != other.y:
                return Inf(self.curve)
            if self.curve == other.curve:
                m = self.__m(self, other)
                x_r = (m**2 - self.x - other.x) % self.p
                y_r = -(self.y + m * (x_r - self.x)) % self.p
                return Point(self.curve, x_r, y_r)
            raise ValueError("Cannot add points belonging to different curves")
        raise TypeError(
            f"Unsupported operand type(s) for +: '{other.__class__.__name__}' and '{self.__class__.__name__}'"
        )

    def __sub__(self, other):
        """
        Subtracts another point or the point at infinity from this point.

        Args:
            other: The point to subtract.

        Returns:
            The result of subtracting the points.

        Raises:
            TypeError if the operand is not a Point or Inf.
        """
        if isinstance(other, Inf):
            return self.__add__(other)
        if isinstance(other, Point):
            return self.__add__(Point(self.curve, other.x, -other.y % self.p))
        raise TypeError(
            f"Unsupported operand type(s) for -: '{other.__class__.__name__}' and '{self.__class__.__name__}'"
        )

    def __mul__(self, other):
        """
        Multiplies the point by a scalar (integer or long type).

        Args:
            other: The scalar to multiply by.

        Returns:
            The result of the point multiplication.

        Raises:
            TypeError if the operand is not an integer or Inf.
        """
        if isinstance(other, Inf):
            return Inf(self.curve)
        if isinstance(other, (int, LONG_TYPE)):
            if other % self.curve.n == 0:
                return Inf(self.curve)
            addend = Point(self.curve, self.x, -self.y % self.p) if other < 0 else self
            result = Inf(self.curve)
            for bit in reversed(bin(abs(other))[2:]):
                if bit == "1":
                    result += addend
                addend += addend
            return result
        raise TypeError(
            f"Unsupported operand type(s) for *: '{other.__class__.__name__}' and '{self.__class__.__name__}'"
        )

    def __rmul__(self, other):
        """
        Multiplies the point by a scalar from the right.

        Args:
            other: The scalar to multiply by.

        Returns:
            The result of the point multiplication.
        """
        return self.__mul__(other)

    def __str__(self) -> str:
        """
        Returns a string representation of the point.

        Returns:
            A string representation of the point on the curve.
        """
        return f"({self.x}, {self.y}) {'on' if self.on_curve else 'off'} {self.curve}"

    def __repr__(self) -> str:
        """
        Returns a more detailed string representation of the point.

        Returns:
            A string representation for debugging.
        """
        return self.__str__()

    def type(self):
        """
        Returns a `PointType` object for serialization.

        Returns:
            A `PointType` object with x and y coordinates as strings.
        """
        return PointType(x=str(self.x), y=str(self.y))


class Inf:
    """
    Represents the point at infinity on the elliptic curve.
    """

    def __init__(self, curve: curve.Curve, x: int = None, y: int = None):
        """
        Initializes the point at infinity.

        Args:
            curve: The elliptic curve this point belongs to.
            x: The x-coordinate (not used for the point at infinity).
            y: The y-coordinate (not used for the point at infinity).
        """
        self.x = x
        self.y = y
        self.curve = curve

    def __eq__(self, other):
        """
        Checks equality between the point at infinity and another point.

        Args:
            other: The object to compare with.

        Returns:
            True if both are point at infinity on the same curve.
        """
        return isinstance(other, Inf) and self.curve == other.curve

    def __ne__(self, other):
        """
        Checks inequality between the point at infinity and another point.

        Args:
            other: The object to compare with.

        Returns:
            True if they are not equal.
        """
        return not self.__eq__(other)

    def __add__(self, other):
        """
        Adds the point at infinity to another point or point at infinity.

        Args:
            other: The point to add.

        Returns:
            The other point since the identity element is the point at infinity.
        """
        if isinstance(other, Inf):
            return Inf(self.curve)
        if isinstance(other, Point):
            return other
        raise TypeError(
            f"Unsupported operand type(s) for +: '{other.__class__.__name__}' and '{self.__class__.__name__}'"
        )

    def __sub__(self, other):
        """
        Subtracts the point at infinity from another point or point at infinity.

        Args:
            other: The point to subtract.

        Returns:
            The other point since subtracting infinity is equivalent to adding it.
        """
        if isinstance(other, Inf):
            return Inf(self.curve)
        if isinstance(other, Point):
            return other
        raise TypeError(
            f"Unsupported operand type(s) for -: '{other.__class__.__name__}' and '{self.__class__.__name__}'"
        )

    def __str__(self) -> str:
        """
        Returns a string representation of the point at infinity.

        Returns:
            A string representation of the point at infinity.
        """
        return f"{self.__class__.__name__} on {self.curve}"

    def __repr__(self) -> str:
        """
        Returns a more detailed string representation of the point at infinity.

        Returns:
            A string representation for debugging.
        """
        return self.__str__()
