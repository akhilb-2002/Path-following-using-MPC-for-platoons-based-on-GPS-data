import math

def add_points(coordinates):
    new_coordinates = []
    for i in range(len(coordinates) - 1):
        x1, y1 = coordinates[i]
        x2, y2 = coordinates[i + 1]

        distance_x = abs(x2 - x1)
        distance_y = abs(y2 - y1)

        new_coordinates.append((x1, y1))

        if distance_x > 20:
            num_points = math.ceil(distance_x / 20)
            x_step = (x2 - x1) / num_points
            for j in range(1, num_points):
                new_coordinates.append((x1 + j * x_step, y1))

        if distance_y > 20:
            num_points = math.ceil(distance_y / 20)
            y_step = (y2 - y1) / num_points
            for j in range(1, num_points):
                new_coordinates.append((x2, y1 + j * y_step))

    new_coordinates.append(coordinates[-1])
    return new_coordinates

# Example usage:
coordinates = [(0, 0), (10, 25), (30, 25), (40, 40)]
new_coordinates = add_points(coordinates)

print("Original Coordinates:", coordinates)
print("Modified Coordinates:", new_coordinates)
