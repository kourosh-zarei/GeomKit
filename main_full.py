from packages.collections import Points
from packages.rendering import easy_plot
from packages.objects import Point, Square

if __name__ == "__main__":
    focal_length = 50
    sensor_width = 36
    sensor_height = 24
    pixel_width = 12
    pixel_height = 8
    unit = 1000
    N = 3

    cameras = Points.get_points_at_inclinations(N, [30, 50], r=2)

    pictures = Square.generate_pictures(
        cameras.elements, focal_length, sensor_width, sensor_height, unit
    )

    pixels = [picture.to_rays(pixel_width, pixel_height, 1, 30) for picture in pictures]

    easy_plot(
        Point.origin(),
        cameras.points,
        pictures,
        pixels,
        window_size=3,
    )
