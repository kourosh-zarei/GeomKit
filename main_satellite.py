from packages.collections import Points
from packages.rendering import easy_plot

density = 250
incl_rotations = 7
azim_rotations = 3

planet = Points.get_points_at_inclinations(100, [i for i in range(0, 180, 40)])
satellite = Points.orbitals(density, incl_rotations, azim_rotations, r=2)
easy_plot(planet.elements, satellite.elements)
