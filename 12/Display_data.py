# Re-importing libraries and reinitializing the plot since the code state has been reset.
import matplotlib.pyplot as plt

# Coordinates to plot
# [[0, 0], [1, 0], [1, 1], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [2, 3], [1, 3], [0, 3], [2, 4]]
# [[0, 4], [1, 4], [1, 5], [0, 5]]
coordinates = [[0, 0], [1, 0], [1, 1], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [2, 3], [1, 3], [0, 3], [2, 4]]

#coord_set = set(tuple(coord) for coord in coordinates)
coord_set = [(0, 1), (2, 4), (0, 0), (1, 1), (0, 3), (2, 3), (0, 2), (2, 2), (1, 0), (3, 2), (1, 3)]

# Plot the grid and points
fig, ax = plt.subplots(figsize=(10, 10))

# Draw the grid
max_x = max(y for x, y in coord_set)
max_y = max(x for x, y in coord_set)
ax.set_xlim(0, max_x + 2)
ax.set_ylim(0, max_y + 2)
ax.set_xticks(range(0, max_x + 3))
ax.set_yticks(range(0, max_y + 3))
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# Draw each point as a square
for (y, x) in coord_set:
    rect = plt.Rectangle((x, y), 1, 1, color="skyblue", ec="black")
    ax.add_patch(rect)

ax.invert_yaxis()
ax.xaxis.tick_top()

# Set aspect ratio and labels
ax.set_aspect('equal')
ax.set_title("Grid Representation of Coordinates")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")

plt.show()