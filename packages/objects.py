import numpy as np
from typing import Optional, Tuple
from packages.utils import pol_to_cart, cart_to_pol, distance


NORMALISE_DEFAULT = True


class Point:
    def __init__(self, a: float, b: float, c: float) -> None:
        self.array = np.array([a, b, c])

    def __neg__(self):
        return Point(*-self.array)

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Point' and '{type(other).__name__}'"
            )
        return Point(*(self.array + other.array))

    def __sub__(self, other):
        if not isinstance(other, Point):
            raise TypeError(
                f"unsupported operand type(s) for -: 'Point' and '{type(other).__name__}'"
            )
        return Point(*(self.array - other.array))

    @property
    def magnitude(self):
        return distance(*self.array)

    @staticmethod
    def from_np(abc: np.ndarray):
        if abc.shape != (3,):
            raise TypeError(
                f"unsupported shape size for Point: expected (3,), got '{abc.shape}'"
            )
        return Point(*abc)

    @staticmethod
    def origin() -> "Point":
        return Point(0, 0, 0)

    @staticmethod
    def right() -> "Point":
        return Point(1, 0, 0)

    @staticmethod
    def forward() -> "Point":
        return Point(0, 1, 0)

    @staticmethod
    def up() -> "Point":
        return Point(0, 0, 1)

    def reflect_on(self, point: "Point") -> "Point":
        return Point(*((2 * point.array) - self.array))

    def move_by(self, other):
        if not isinstance(other, Vector):
            raise TypeError(
                f"unsupported operand type(s) for move_by: 'Point' and '{type(other).__name__}'"
            )
        return Point(*(self.array + other.direction.array))

    @property
    def vector(self) -> "Vector":
        return Vector(*self.array, start_point=Point.origin())


class Vector:
    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        start_point: Optional[Point] = None,
        normalise: bool = NORMALISE_DEFAULT,
    ):
        try:
            self.direction = Point(
                *(np.array([x, y, z]) / (distance(x, y, z) if normalise else 1))
            )
            self.start = start_point if start_point is not None else Point.origin()
        except ZeroDivisionError:
            raise ZeroDivisionError("Vector must have non-zero length")

    def __neg__(self):
        return Vector(*-self.direction.array, start_point=self.start)

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Vector' and '{type(other).__name__}'"
            )
        return Vector(
            *(self.direction.array + other.direction.array),
            start_point=self.start + other.start,
        )

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError(
                f"unsupported operand type(s) for -: 'Vector' and '{type(other).__name__}'"
            )
        return Vector(
            *(self.direction.array - other.direction.array),
            self.start.array - other.start.array,
        )

    @staticmethod
    def right():
        return Vector(*Point.right().array)

    @staticmethod
    def forward():
        return Vector(*Point.forward().array)

    @staticmethod
    def up():
        return Vector(*Point.up().array)

    @property
    def magnitude(self) -> float:
        return distance(*self.direction.array)

    @property
    def end(self) -> Point:
        return Point(*(self.direction.array+self.start.array))

    def at_t(self, t: float) -> Point:
        return Point.from_np(t * self.direction.array + self.start.array)

    def offset_to(self, offset_point: Point) -> "Vector":
        return Vector(*self.direction.array, start_point=offset_point)

    def offset_by(self, offset_point: Point) -> "Vector":
        return Vector(
            *self.direction.array,
            start_point=self.start.array + offset_point.array,
        )

    def shrink_to(self, length: float) -> "Vector":
        direction = self.direction.array * length / self.magnitude
        return Vector(*direction, start_point=self.start)

    def shrink_by(self, length: float) -> "Vector":
        direction = self.direction.array * (self.magnitude - length) / self.magnitude
        return Vector(*direction, start_point=self.start)

    @staticmethod
    def from_polar(
        r: float,
        incl: float,
        azim: float,
        start_point: Point = None,
        normalise=NORMALISE_DEFAULT,
    ) -> "Vector":
        x, y, z = pol_to_cart(r, incl, azim)
        return Vector(x, y, z, start_point=Point(0,0,0) if start_point is None else start_point, normalise=normalise)

    def to_polar(self) -> np.ndarray:
        return np.array(cart_to_pol(*self.direction.array))

    @staticmethod
    def intersects(v1: "Vector", v2: "Vector") -> Point:
        x1, y1, z1 = v1.direction.array
        a1, b1, c1 = v1.start.array
        x2,y2,z2 = v2.direction.array
        a2,b2,c2 = v2.start.array
        intersection_x = (a2 - a1) / (x1 - x2)
        intersection_y = (b2 - b1) / (y1 - y2)
        intersection_z = (c2 - c1) / (z1 - z2)
        return Point(intersection_x, intersection_y, intersection_z)

    @staticmethod
    def cross_product(v1: "Vector", v2: "Vector", normalise=NORMALISE_DEFAULT):
        return Vector(
            *np.cross(v1.direction.array, v2.direction.array),
            start_point=Point(*(v1.start.array+v2.start.array)),
            normalise=normalise
        ).offset_to(Vector.intersects(v1, v2))


class Line:
    def __init__(
        self, start_point: Optional[Point] = None, end_point: Optional[Point] = None
    ) -> None:
        self.start = start_point
        self.end = end_point

    @staticmethod
    def from_(start_point: Point) -> "AmbiguousLine":
        return AmbiguousLine(start_point)

    @staticmethod
    def to(end_point: Point) -> "Line":
        return Line(end_point=end_point)

    @property
    def vector(self, normalise=False) -> "Vector":
        return Vector(
            *(self.end.array - self.start.array),
            start_point=self.start,
            normalise=normalise,
        )

    def length(self) -> float:
        return distance(*(self.end.array - self.start.array))


class AmbiguousLine:
    def __init__(self, start_point: Point):
        self.start = start_point

    def to(self, end_point: Point) -> Line:
        return Line(self.start, end_point)


class Surface:
    def __init__(self, a: float, b: float, c: float, d: float) -> None:
        """Ax + By + Cz + D = 0"""
        if a == b == c == 0:
            raise ValueError(
                "Invalid surface: coefficients a, b, and c cannot all be zero."
            )
        self.a, self.b, self.c, self.d = a, b, c, d

    @property
    def coefficients(self) -> np.ndarray:
        return np.array([self.a, self.b, self.c, self.d])

    @staticmethod
    def is_perpendicular_to_at(vector: Vector, point: Point) -> "Surface":
        a, b, c = vector.direction.array
        x0, y0, z0 = point.array
        d = -(a * x0 + b * y0 + c * z0)
        return Surface(a, b, c, d)

    def intersects(self, vector: Vector) -> Point:
        a, b, c, d = self.coefficients
        plane_normal = np.array([a, b, c])
        plane_point = -d * plane_normal / (np.linalg.norm(plane_normal) ** 2)
        vector_direction = vector.direction.array
        vector_point = vector.start.array
        t = np.dot((plane_point - vector_point), plane_normal) / np.dot(
            vector_direction, plane_normal
        )
        return Point.from_np(t * vector_direction + vector_point)

    def to_mesh(self, surface_size: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        a, b, c, d = self.coefficients
        coord = np.linspace(-surface_size, surface_size, 10)
        if a != 0:
            mg_y, mg_z = np.meshgrid(-coord, coord)
            mg_x = (-b * mg_y - c * mg_z - d) / a
        elif b != 0:
            mg_x, mg_z = np.meshgrid(-coord, coord)
            mg_y = (-a * mg_x - c * mg_z - d) / b
        else:
            mg_x, mg_y = np.meshgrid(-coord, coord)
            mg_z = (-a * mg_x - b * mg_y - d) / c
        return mg_x, mg_y, mg_z


class Square:
    def __init__(self, ab, bc, cd, da):
        self.ab, self.bc, self.cd, self.da = ab, bc, cd, da
