from packages.rendering import easy_plot
from packages.objects import Point, Square, Line

if __name__ == "__main__":
    focal_length = 6
    width = 36
    height = 24

    point = Point(10, 10, 10)
    picture = Square.generate_picture(
        point,
        focal_length,
        width,
        height,
    )

    easy_plot(
        Point.origin(),
        picture.source,
        picture,
        # rays,
        window_size=12,
    )
