from typing import List
from packages.objects import Point, Vector, Surface


class Points:
    def __init__(self, points: List[Point]):
        self.points = points

    def __iter__(self):
        return iter(self.points)

    @property
    def elements(self):
        return self.points

    @staticmethod
    def get_points_at_incl(
        num_samples: int, incl: float, r: float = 1, normalise: bool = False
    ) -> "Points":
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
    ) -> "Points":
        incl_range = range(0, incl_rotations * 360 * density, incl_rotations * 360)
        azim_range = range(0, azim_rotations * 360 * density, azim_rotations * 360)
        inclinations = [incl / density for incl in incl_range]
        azimuths = [azimuth / density for azimuth in azim_range]
        points = [
            Vector.from_polar(r, inclination, azimuth).point
            for inclination, azimuth in zip(inclinations, azimuths)
        ]
        return Points(points)


class AmbiguousSurfaces:
    def __init__(self, vectors: List[Vector]):
        self.vectors = vectors

    def at(self, points: List[Point]) -> "Surfaces":
        surfaces = [
            Surface.intersects(vector).at(point)
            for vector, point in zip(self.vectors, points)
        ]
        return Surfaces(surfaces)


class Surfaces:
    def __init__(self, surfaces: List[Surface]):
        self.surfaces = surfaces

    def __iter__(self):
        return iter(self.surfaces)

    @property
    def elements(self):
        return self.surfaces

    @staticmethod
    def intersect(vectors: List[Vector]) -> AmbiguousSurfaces:
        return AmbiguousSurfaces(vectors)
