import json
from collections import defaultdict
from typing import Optional, Tuple, List
import numpy as np
from packages.utils import distance, pol_to_cart, cart_to_pol


NORMALISE_DEFAULT = True


class Point:
    """
    This class represents a 3D point in space. The point is defined by three coordinates (a, b, c).
    """

    def __init__(self, a: float, b: float, c: float, name: str = None) -> None:
        """
        Constructor for a Point object.

        Parameters:
        a (float): x-coordinate of the point.
        b (float): y-coordinate of the point.
        c (float): z-coordinate of the point.
        """

        self.array = np.array([a, b, c])
        self.name = name

    def __str__(self):
        """
        Returns a string representation of the Point.

        Returns:
        str: A string representation of the Point.
        """

        return str(self.array)

    def __neg__(self):
        """
        Defines the negation of a Point object, reversing the sign of each of its coordinates.

        Returns:
        Point: A new Point object with reversed coordinates.
        """

        return Point(*-self.array)

    def __add__(self, other):
        """
        Defines the addition of two Point objects.

        Parameters:
        other (Point): Another Point object.

        Returns:
        Point: A new Point object resulting from the addition of two Point objects.

        Raises:
        TypeError: If the other object is not an instance of Point.
        """

        if not isinstance(other, Point):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Point' and '{type(other).__name__}'"
            )
        return Point(*(self.array + other.array))

    def __sub__(self, other):
        """
        Defines the subtraction of two Point objects.

        Parameters:
        other (Point): Another Point object.

        Returns:
        Point: A new Point object resulting from the subtraction of two Point objects.

        Raises:
        TypeError: If the other object is not an instance of Point.
        """

        if not isinstance(other, Point):
            raise TypeError(
                f"unsupported operand type(s) for -: 'Point' and '{type(other).__name__}'"
            )
        return Point(*(self.array - other.array))

    @property
    def magnitude(self):
        """
        Calculates the magnitude (distance from the origin) of the Point.

        Returns:
        float: The magnitude of the Point.
        """

        return distance(*self.array)

    @staticmethod
    def from_np(abc: np.ndarray, name: str = None):
        """
        Static method to create a Point object from a numpy array.

        Parameters:
        abc (np.ndarray): A numpy array with shape (3,).

        Returns:
        Point: A new Point object.

        Raises:
        TypeError: If the input array does not have shape (3,).
        """

        if abc.shape != (3,):
            raise TypeError(
                f"unsupported shape size for Point: expected (3,), got '{abc.shape}'"
            )
        return Point(*abc, name=name)

    @staticmethod
    def origin() -> "Point":
        """
        Static method that returns a Point object at the origin.

        Returns:
        Point: A new Point object at the origin (0, 0, 0).
        """

        return Point(0, 0, 0)

    @staticmethod
    def right() -> "Point":
        """
        Static method that returns a Point object at the right direction along the x-axis.

        Returns:
        Point: A new Point object at (1, 0, 0).
        """

        return Point(1, 0, 0)

    @staticmethod
    def forward() -> "Point":
        """
        Static method that returns a Point object in the forward direction along the y-axis.

        Returns:
        Point: A new Point object at (0, 1, 0).
        """

        return Point(0, 1, 0)

    @staticmethod
    def up() -> "Point":
        """
        Static method that returns a Point object in the up direction along the z-axis.

        Returns:
        Point: A new Point object at (0, 0, 1).
        """

        return Point(0, 0, 1)

    def reflect_on(self, point: "Point") -> "Point":
        """
        Reflects the Point on another point.

        Parameters:
        point (Point): The point on which to reflect.

        Returns:
        Point: A new Point object that is the reflection of the original Point.
        """

        return Point(*((2 * point.array) - self.array))

    def move_by(self, other):
        """
        Moves the Point by a Vector.

        Parameters:
        other (Vector): The vector by which to move the Point.

        Returns:
        Point: A new Point object resulting from moving the original Point by the Vector.

        Raises:
        TypeError: If the other object is not an instance of Vector.
        """

        if not isinstance(other, Vector):
            raise TypeError(
                f"unsupported operand type(s) for move_by: 'Point' and '{type(other).__name__}'"
            )
        return Point(*(self.array + other.direction.array))

    def vector(self, normalise=False) -> "Vector":
        """
        Returns a vector that represents the Point, with its tail at the origin and its head at the Point.

        Parameters:
        normalise (bool): If True, the returned vector will be normalised to have a length of 1.

        Returns:
        Vector: A new Vector object that represents the Point.
        """

        return Vector(*self.array, start_point=Point.origin(), normalise=normalise)


class Line:
    """
    A class representing a line in 3D space, defined by a start point and an end point.
    """

    def __init__(
        self,
        start_point: Optional[Point] = None,
        end_point: Optional[Point] = None,
        name: str = None,
    ) -> None:
        """
        Creates a new Line object.

        Parameters:
        start_point (Optional[Point]): The starting point of the line. If None, the start point is not defined.
        end_point (Optional[Point]): The end point of the line. If None, the end point is not defined.
        """

        self.start = start_point
        self.end = end_point
        self.name = name

    @staticmethod
    def from_(start_point: Point) -> "AmbiguousLine":
        """
        Static method that creates an AmbiguousLine object with a defined start point.

        Parameters:
        start_point (Point): The start point of the line.

        Returns:
        AmbiguousLine: A new AmbiguousLine object with a defined start point.
        """

        return AmbiguousLine(start_point)

    @staticmethod
    def to(end_point: Point) -> "Line":
        """
        Static method that creates a Line object with a defined end point.

        Parameters:
        end_point (Point): The end point of the line.

        Returns:
        Line: A new Line object with a defined end point.
        """

        return Line(end_point=end_point)

    def vector(self, normalise=False) -> "Vector":
        """
        Converts the line to a Vector object.

        Parameters:
        normalise (bool): If True, the resulting vector is normalised to have a length of 1.

        Returns:
        Vector: A new Vector object representing the direction and length of the line.
        """

        return Vector(
            *(self.end.array - self.start.array),
            start_point=self.start,
            normalise=normalise,
        )

    def length(self) -> float:
        """
        Returns the length of the line.

        Returns:
        float: The length of the line.
        """

        return distance(*(self.end.array - self.start.array))

    def to_mesh(self, density: int, subject_radius: float) -> List[Point]:
        x1, y1, z1 = self.start.array
        x2, y2, z2 = self.end.array
        points = np.column_stack(
            (
                np.linspace(x1, x2, density),
                np.linspace(y1, y2, density),
                np.linspace(z1, z2, density),
            )
        )
        points = [Point.from_np(point, self.name) for point in points]
        points = [
            point for point in points if distance(*point.array) < (subject_radius * 1.2)
        ]
        return points

    def with_name(self, name: str):
        self.name = name
        return self


class AmbiguousLine:
    """
    A class representing a line in 3D space with a defined start point but undefined end point.
    """

    def __init__(self, start_point: Point):
        """
        Creates a new AmbiguousLine object.

        Parameters:
        start_point (Point): The start point of the line.
        """

        self.start = start_point

    def to(self, end_point: Point) -> Line:
        """
        Defines the end point of the AmbiguousLine object, converting it into a Line object.

        Parameters:
        end_point (Point): The end point of the line.

        Returns:
        Line: A new Line object with defined start and end points.
        """

        return Line(self.start, end_point)


class Vector:
    """
    This class represents a 3D vector in space. A vector is defined by its direction and start point.
    """

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        start_point: Optional[Point] = None,
        normalise: bool = NORMALISE_DEFAULT,
    ):
        """
        Constructor for a Vector object.

        Parameters:
        x (float): x-direction of the vector.
        y (float): y-direction of the vector.
        z (float): z-direction of the vector.
        start_point (Optional[Point]): The start point of the vector. If None, the start point is the origin.
        normalise (bool): If True, the created vector is normalised to have a length of 1.

        Raises:
        ZeroDivisionError: If the provided direction vector has zero length and normalisation is requested.
        """

        try:
            self.direction = Point(
                *(np.array([x, y, z]) / (distance(x, y, z) if normalise else 1))
            )
            self.start = start_point if start_point is not None else Point.origin()
        except ZeroDivisionError:
            raise ZeroDivisionError("Vector must have non-zero length")

    def __neg__(self):
        """
        Defines the negation of a Vector object, reversing its direction.

        Returns:
        Vector: A new Vector object with reversed direction.
        """

        return Vector(*(-self.direction).array, start_point=self.start, normalise=False)

    def __add__(self, other):
        """
        Defines the addition of two Vector objects.

        Parameters:
        other (Vector): Another Vector object.

        Returns:
        Vector: A new Vector object resulting from the addition of two Vector objects.

        Raises:
        TypeError: If the other object is not an instance of Vector.
        """

        if not isinstance(other, Vector):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Vector' and '{type(other).__name__}'"
            )
        return Vector(
            *(self.direction.array + other.direction.array),
            start_point=self.start + other.start,
        )

    def __sub__(self, other):
        """
        Defines the subtraction of two Vector objects.

        Parameters:
        other (Vector): Another Vector object.

        Returns:
        Vector: A new Vector object resulting from the subtraction of two Vector objects.

        Raises:
        TypeError: If the other object is not an instance of Vector.
        """

        if not isinstance(other, Vector):
            raise TypeError(
                f"unsupported operand type(s) for -: 'Vector' and '{type(other).__name__}'"
            )
        return Vector(
            *(self.direction.array - other.direction.array),
            self.start.array - other.start.array,
        )

    def __mul__(self, other):
        if not (isinstance(other, int) or isinstance(other, float)):
            raise TypeError(
                f"unsupported operand type(s) for -: 'Vector' and '{type(other).__name__}'"
            )
        return Vector(
            *(self.direction.array * other), start_point=self.start, normalise=False
        )

    @property
    def line(self) -> Line:
        return Line.from_(self.start).to(self.end)

    @staticmethod
    def right():
        """
        Static method that returns a Vector object in the right direction along the x-axis.

        Returns:
        Vector: A new Vector object in the right direction.
        """

        return Vector(*Point.right().array)

    @staticmethod
    def forward():
        """
        Static method that returns a Vector object in the forward direction along the y-axis.

        Returns:
        Vector: A new Vector object in the forward direction.
        """

        return Vector(*Point.forward().array)

    @staticmethod
    def up():
        """
        Static method that returns a Vector object in the up direction along the z-axis.

        Returns:
        Vector: A new Vector object in the up direction.
        """

        return Vector(*Point.up().array)

    @property
    def magnitude(self) -> float:
        """
        Property that returns the magnitude (length) of the Vector object.

        Returns:
        float: The magnitude of the vector.
        """

        return distance(*self.direction.array)

    @property
    def end(self) -> Point:
        """
        Property that returns the end point of the Vector object.

        Returns:
        Point: The end point of the vector.
        """

        return Point(*(self.direction.array + self.start.array))

    def at_t(self, t: float) -> Point:
        """
        Returns the point at a certain distance along the vector, from its start point.

        Parameters:
        t (float): The distance along the vector.

        Returns:
        Point: The point at distance "t" from the start point along the vector.
        """

        return Point.from_np(t * self.direction.array + self.start.array)

    def offset_to(self, offset_point: Point) -> "Vector":
        """
        Returns a new Vector object with the same direction as the original but starting from a new start point.

        Parameters:
        offset_point (Point): The new start point for the vector.

        Returns:
        Vector: The new Vector object starting from 'offset_point'.
        """

        return Vector(*self.direction.array, start_point=offset_point)

    def offset_by(self, offset_point: Point) -> "Vector":
        """
        Returns a new Vector object with the same direction as the original but its start point is moved by a
        specified Point.

        Parameters:
        offset_point (Point): The point by which to offset the start point of the vector.

        Returns:
        Vector: The new Vector object with its start point offset by 'offset_point'.
        """

        return Vector(
            *self.direction.array,
            start_point=self.start.array + offset_point.array,
        )

    def change_size_to(self, length: float) -> "Vector":
        """
        Returns a new Vector object with the same direction as the original but with a specified length.

        Parameters:
        length (float): The new length for the vector.

        Returns:
        Vector: The new Vector object with length 'length'.
        """

        v = Vector(*self.direction.array, start_point=self.start, normalise=True)
        new_direction = v.direction.array * length
        return Vector(*new_direction, start_point=self.start, normalise=False)

    def shrink_by(self, length: float) -> "Vector":
        """
        Returns a new Vector object with the same direction as the original but its length is reduced by a specified
        amount.

        Parameters:
        length (float): The amount by which to reduce the length of the vector.

        Returns:
        Vector: The new Vector object with its length reduced by 'length'.
        """

        direction = self.direction.array * (self.magnitude - length) / self.magnitude
        return Vector(*direction, start_point=self.start, normalise=False)

    @staticmethod
    def from_polar(
        r: float,
        incl: float,
        azim: float,
        start_point: Point = None,
        normalise=NORMALISE_DEFAULT,
    ) -> "Vector":
        """
        Static method that creates a Vector object from polar coordinates.

        Parameters:
        r (float): The radial distance.
        incl (float): The inclination angle (from the positive z-axis).
        azim (float): The azimuth angle (from the positive x-axis in the x-y plane).
        start_point (Optional[Point]): The start point for the vector. If None, the start point is the origin.
        normalise (bool): If True, the created vector is normalised to have a length of 1.

        Returns:
        Vector: The new Vector object created from the given polar coordinates.
        """

        x, y, z = pol_to_cart(r, incl, azim)
        start_point = Point(0, 0, 0) if start_point is None else start_point
        return Vector(x, y, z, start_point=start_point, normalise=normalise)

    def to_polar(self) -> np.ndarray:
        """
        Converts the direction of the Vector object to polar coordinates.

        Returns:
        np.ndarray: An array of polar coordinates [r, incl, azim].
        """

        return np.array(cart_to_pol(*self.direction.array))

    @staticmethod
    def intersects(v1: "Vector", v2: "Vector") -> Point:
        """
        Static method that finds the intersection point of two vectors, if it exists.

        Parameters:
        v1 (Vector): The first vector.
        v2 (Vector): The second vector.

        Returns:
        Point: The point of intersection of the two vectors.

        Note: This method assumes that the vectors intersect. If they don't intersect, the result will not be
        meaningful.
        """

        x1, y1, z1 = v1.direction.array
        a1, b1, c1 = v1.start.array
        x2, y2, z2 = v2.direction.array
        a2, b2, c2 = v2.start.array
        intersection_x = (a2 - a1) / (x1 - x2)
        intersection_y = (b2 - b1) / (y1 - y2)
        intersection_z = (c2 - c1) / (z1 - z2)
        return Point(intersection_x, intersection_y, intersection_z)

    @staticmethod
    def cross_product(
        v1: "Vector", v2: "Vector", normalise=NORMALISE_DEFAULT
    ) -> "Vector":
        """
        Static method that calculates the cross product of two Vector objects.

        Parameters:
        v1 (Vector): The first vector.
        v2 (Vector): The second vector.
        normalise (bool): If True, the resulting vector is normalised to have a length of 1.

        Returns:
        Vector: A new Vector object that is the cross product of v1 and v2.
        """

        cross = np.cross(v1.direction.array, v2.direction.array)
        return Vector(*cross, start_point=v1.start + v2.start, normalise=normalise)


class Square:
    """
    A class representing a square in 3D space, defined by four points.
    """

    def __init__(
        self,
        a: Point,
        b: Point,
        c: Point,
        d: Point,
        source_point: Point,
        name: str = None,
    ):
        """
        Creates a new Square object.

        Parameters:
        a, b, c, d (Point): The vertices of the square. The graph connecting the points should follow
                            the order a -> b -> c -> d -> a.
        """

        self.a, self.b, self.c, self.d = a, b, c, d
        self.source = source_point
        self.name = name

    @staticmethod
    def generate_picture(
        camera: Point,
        focal_length: float = 50,
        width: float = 36,
        height: float = 24,
        unit: float = 1_000,
        name: str = None,
    ) -> "Square":
        """
        Static method that generates a picture of the Square object as seen from a camera.

        Parameters:
        camera (Point): The location of the camera in 3D space.
        focal_length (float): The focal length of the camera (in mm).
        width (float): The width of the picture (in mm).
        height (float): The height of the picture (in mm).
        unit (float): The unit of length used in the picture (mm)

        Returns:
        Square: A new Square object representing the picture of the original Square as seen from the camera.
        """

        center = camera.vector().shrink_by(focal_length / 1000).end
        camera_plane = Plane.is_perpendicular_to_at(camera.vector(), center)
        up_intersects_camera_point = camera_plane.intersects(Vector.up())
        m_u = (
            Line.from_(center)
            .to(up_intersects_camera_point)
            .vector(True)
            .change_size_to(height / (2 * unit))
        )
        m_rl = Vector.cross_product(m_u, camera.vector()).change_size_to(
            width / (2 * unit)
        )
        a = center.move_by(m_u).move_by(-m_rl)
        b = center.move_by(m_u).move_by(m_rl)
        c = center.move_by(-m_u).move_by(m_rl)
        d = center.move_by(-m_u).move_by(-m_rl)
        return Square(a, b, c, d, camera, name)

    def to_mesh(self):
        """
        Converts the Square object to a mesh representation.

        Returns:
        tuple: A tuple containing three lists representing the x, y, and z coordinates of the vertices of the square.
        """

        matrix = np.array(
            [self.a.array, self.b.array, self.c.array, self.d.array, self.a.array]
        ).T
        x = matrix[0].tolist()
        y = matrix[1].tolist()
        z = matrix[2].tolist()
        return x, y, z

    def to_pixel_array(self, pixel_width, pixel_height) -> List[Point]:
        width_steps = np.linspace(0, 1, pixel_width)
        height_steps = np.linspace(0, 1, pixel_height)
        pixels = []
        for w_ind, ws in enumerate(width_steps):
            for h_ind, hs in enumerate(height_steps):
                top = (1 - ws) * self.a.array + ws * self.b.array
                bottom = (1 - ws) * self.d.array + ws * self.c.array
                pixel = (1 - hs) * top + hs * bottom
                pixels.append(
                    Point.from_np(pixel, f"img_{self.name} w_{w_ind} h_{h_ind}")
                )
        return pixels

    def to_rays(self, pixel_width, pixel_height, ray_length: float) -> List[Line]:
        pixels = self.to_pixel_array(pixel_width, pixel_height)
        return [
            (
                Line.from_(self.source).to(pixel).vector(True) * ray_length
            ).line.with_name(pixel.name)
            for pixel in pixels
        ]


class Plane:
    """
    A class representing a plane in 3D space, defined by the equation Ax + By + Cz + D = 0.
    """

    def __init__(self, a: float, b: float, c: float, d: float) -> None:
        """
        Creates a new Plane object.

        Parameters:
        a, b, c, d (float): The coefficients in the plane equation.

        Raises:
        ValueError: If a, b, and c are all zero, which would make the equation invalid.
        """

        if a == b == c == 0:
            raise ValueError(
                "Invalid plane: coefficients a, b, and c cannot all be zero."
            )
        self.a, self.b, self.c, self.d = a, b, c, d

    @property
    def coefficients(self) -> np.ndarray:
        """
        Returns the coefficients of the plane equation.

        Returns:
        np.ndarray: A numpy array containing the coefficients [a, b, c, d].
        """

        return np.array([self.a, self.b, self.c, self.d])

    @staticmethod
    def is_perpendicular_to_at(vector: Vector, point: Point) -> "Plane":
        """
        Static method that creates a new Plane object that is perpendicular to a given vector at a given point.

        Parameters:
        vector (Vector): The vector to which the plane is perpendicular.
        point (Point): The point at which the plane intersects the vector.

        Returns:
        Plane: The new Plane object.
        """

        a, b, c = vector.direction.array
        x0, y0, z0 = point.array
        d = -(a * x0 + b * y0 + c * z0)
        return Plane(a, b, c, d)

    def intersects(self, vector: Vector) -> Point:
        """
        Finds the point of intersection between the plane and a given vector.

        Parameters:
        vector (Vector): The vector with which to find an intersection.

        Returns:
        Point: The point of intersection.
        """

        a, b, c, d = self.coefficients
        plane_normal = np.array([a, b, c])
        plane_point = -d * plane_normal / (np.linalg.norm(plane_normal) ** 2)
        vector_direction = vector.direction.array
        vector_point = vector.start.array
        t = np.dot((plane_point - vector_point), plane_normal) / np.dot(
            vector_direction, plane_normal
        )
        return Point.from_np(t * vector_direction + vector_point)

    def to_mesh(self, plane_size: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Converts the Plane object to a mesh representation.

        Parameters:
        plane_size (float): The size of the plane.

        Returns: tuple: A tuple containing three numpy arrays representing the x, y, and z coordinates of the
        vertices of the plane.
        """

        a, b, c, d = self.coefficients
        coord = np.linspace(-plane_size, plane_size, 10)
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


class SubSpace:
    """
    An object representing the subspace division concept of this project.
    The aim of this object is to store ray objects and identify to which subspaces each ray belongs to.
    """

    def __init__(self, subspace_divisions: int, length: float = 1):
        self.subspace_assignments = defaultdict(set)
        if subspace_divisions == 1:
            self.points = [Point.origin()]
        else:
            length_division = np.linspace(-length / 2, length / 2, subspace_divisions)
            self.points = [
                [x, y, z]
                for x in length_division
                for y in length_division
                for z in length_division
            ]

    def json(self):
        json.load()

    # def save(self):
    #     json.
