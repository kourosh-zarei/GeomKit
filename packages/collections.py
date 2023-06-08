from typing import List
from packages.objects import Point, Vector, Plane


class Points:
    """
    A class representing a collection of points in 3D space.
    """

    def __init__(self, points: List[Point]):
        """
        Creates a new Points object.

        Parameters:
        points (List[Point]): A list of Point objects.
        """

        self.points = points

    def __iter__(self):
        """
        Returns an iterator over the points in the collection.
        """

        return iter(self.points)

    @property
    def elements(self):
        """
        Returns the list of points in the collection.
        """

        return self.points

    @staticmethod
    def get_points_at_incl(
        num_samples: int, incl: float, r: float = 1, normalise: bool = False
    ) -> "Points":
        """
        Static method to get a list of points at a certain inclination.

        Parameters:
        num_samples (int): The number of points to generate.
        incl (float): The inclination angle in degrees.
        r (float, optional): The radius, defaults to 1.
        normalise (bool, optional): Whether to normalise the points, defaults to False.

        Returns:
        Points: The generated Points object.
        """

        if incl < 5:
            points = [Vector.from_polar(r, 0, 0, normalise=normalise).direction]
        elif 175 < incl:
            points = [Vector.from_polar(r, 180, 0, normalise=normalise).direction]
        else:
            azimuth_samples = [i * 360 / num_samples for i in range(num_samples + 1)]
            points = [
                Vector.from_polar(r, incl, azimuth, normalise=normalise).direction
                for azimuth in azimuth_samples
            ]
        return Points(points)

    @staticmethod
    def get_points_at_inclinations(
        num_samples: int,
        inclinations: List[float],
        r: float = 1,
        normalise: bool = False,
    ) -> "Points":
        """
        This method is used to create a collection of points on a sphere at specific inclinations (in degrees).

        Parameters:
        num_samples (int): The number of points to be generated at each inclination.
        inclinations (List[float]): The list of inclinations (in degrees) at which points are to be generated.
        r (float, optional): The radius of the sphere, defaults to 1.
        normalise (bool, optional): If True, the points are normalised, defaults to False.

        Returns:
        Points: A collection of points at the specified inclinations.
        """

        points = [
            point
            for inclination in inclinations
            for point in Points.get_points_at_incl(
                num_samples, inclination, r, normalise
            )
        ]
        return Points(points)

    @staticmethod
    def orbitals(
        density: int,
        incl_rotations: int,
        azim_rotations: int,
        r: float = 1,
        normalise: bool = False,
    ) -> "Points":
        """
        This method generates a set of points on a sphere that mimic the distribution of points on atomic orbitals.

        Parameters:
        density (int): The number of points per degree.
        incl_rotations (int): The number of rotations in the inclination plane.
        azim_rotations (int): The number of rotations in the azimuth plane.
        r (float, optional): The radius of the sphere, defaults to 1.
        normalise (bool, optional): If True, the points are normalised, defaults to False.

        Returns:
        Points: A collection of points distributed like atomic orbitals.
        """

        incl_range = range(0, incl_rotations * 360 * density, incl_rotations * 360)
        azim_range = range(0, azim_rotations * 360 * density, azim_rotations * 360)
        inclinations = [incl / density for incl in incl_range]
        azimuths = [azimuth / density for azimuth in azim_range]
        points = [
            Vector.from_polar(r, inclination, azimuth, normalise=normalise).end
            for inclination, azimuth in zip(inclinations, azimuths)
        ]
        return Points(points)


class AmbiguousPlanes:
    """
    A class representing a collection of vectors that define ambiguous planes in 3D space.
    """

    def __init__(self, vectors: List[Vector]):
        """
        Creates a new AmbiguousPlanes object.

        Parameters:
        vectors (List[Vector]): A list of Vector objects that define the ambiguous planes.
        """

        self.vectors = vectors

    def at(self, points: List[Point]) -> "Planes":
        """
        This method generates a collection of planes defined by the intersection of the vectors in this object with
        the given points.

        Parameters:
        points (List[Point]): A list of points with which the vectors should intersect.

        Returns:
        Planes: A collection of planes at the given points.
        """

        planes = [
            Plane.intersects(vector).at(point)
            for vector, point in zip(self.vectors, points)
        ]
        return Planes(planes)


class Planes:
    """
    A class representing a collection of planes in 3D space.
    """

    def __init__(self, planes: List[Plane]):
        """
        Creates a new Planes object.

        Parameters:
        planes (List[Plane]): A list of Plane objects.
        """

        self.planes = planes

    def __iter__(self):
        """
        Returns an iterator over the planes in the collection.
        """

        return iter(self.planes)

    @property
    def elements(self):
        """
        Returns the list of planes in the collection.
        """

        return self.planes

    @staticmethod
    def intersect(vectors: List[Vector]) -> AmbiguousPlanes:
        """
        This method creates an AmbiguousPlanes object from a list of vectors. Each vector will define a plane where it intersects with other vectors.

        Parameters:
        vectors (List[Vector]): A list of vectors to create intersections.

        Returns:
        AmbiguousPlanes: A collection of planes created from the intersections of the vectors.
        """

        return AmbiguousPlanes(vectors)
