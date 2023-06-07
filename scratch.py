import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Sensor dimensions (real width and height)
W = 1800  # mm
H = 1200  # mm

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Define the sensor rectangle vertices
vertices = [
    [0, 0, 0],  # Bottom left corner
    [W, 0, 0],  # Bottom right corner
    [W, H, 0],  # Top right corner
    [0, H, 0],  # Top left corner
    [0, 0, 0],  # Bottom left corner (to close the rectangle)
]

# Plot the sensor rectangle
xs, ys, zs = zip(*vertices)
ax.plot(xs, ys, zs)

# Set labels and title
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
ax.set_title("Pinhole Camera Sensor")

# Set aspect ratio
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio for x, y, and z axes

# Show the plot
plt.show()
