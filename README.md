# GeomKit

GeomKit is a specialized package designed to provide robust analytical capabilities for cameras operating in 3D spaces.

**Primary Objective**: To determine which pixels of given images are crucial for reconstructing the scene in voxels.

## Installation and Setup

### Step 1: Clone and Setup
Clone the repository and navigate into the project directory. Once there, run the following command to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

### Step 2: Import and Utilize
With GeomKit, you can effortlessly compute camera configurations and visualization. Below is a basic example of how you can utilize the library:

```python
from GeomKit import Point, Points, Squares
from GeomKit.rendering import easy_plot

subject_radius, camera_radius = 1, 3
cams_along_inclination, inclinations_range = 1, [15, 45, 75]

focal_length = 50
unit = 10  # mm scaled up so you can see the sensors
sensor_width, sensor_height = 36, 24
pixel_width, pixel_height = 6, 4

cameras = Points.get_points_at_inclinations(
    camera_radius, cams_along_inclination, inclinations_range
)

pictures = Squares.generate_pictures(
    cameras, focal_length, sensor_width, sensor_height, unit
)

easy_plot(
    Point.origin(),
    cameras.elements,
    subspace,
    window_size=5,
    subject_radius=subject_radius,
    show_surface=False,
)
```

### Step 3: Dive Deeper with Demos
For a comprehensive overview and understanding, it's advised to execute the code inside main.py. This will offer you a hands-on demonstration of the library's expansive capabilities.

Authors: Kourosh Zarei & King's AI Team

Thank you for choosing GeomKit! We hope it assists you in your 3D camera analysis endeavors.
