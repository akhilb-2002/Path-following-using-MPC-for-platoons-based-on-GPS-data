import xml.etree.ElementTree as ET
import math
from math import inf
import csv
import numpy as np


def latlon_to_xy(point, origin):
    lon_diff = point[0] - origin[0]
    lat_diff = point[1] - origin[1]

    # Assuming 1 degree of latitude is approximately 111 kilometers
    # and 1 degree of longitude is approximately 111 kilometers at the equator
    # Adjust for curvature by using the calculated curvature
    x = lon_diff * 111321.0
    y = lat_diff * 111000.0

    return x, y

def dumfunc():
    # Load the KML file
    kml_file = "BANMAA.kml"
    tree = ET.parse(kml_file)
    root = tree.getroot()

    # Define a namespace dictionary for KML
    kml_namespace = {"kml": "http://www.opengis.net/kml/2.2"}

    # Find the KML Placemark containing the route coordinates
    placemark = root.find(".//kml:Placemark", namespaces=kml_namespace)
    coordinates_element = placemark.find(".//kml:coordinates", namespaces=kml_namespace)

    # Extract and split the coordinates into a list of (latitude, longitude) pairs
    coordinates_text = coordinates_element.text.strip()
    coordinates_list = [tuple(map(float, coord.split(','))) for coord in coordinates_text.split()]

    origin = coordinates_list[0]
    xy_coordinates = [latlon_to_xy(coord, origin) for coord in coordinates_list]
    

    # Remove the last two points from the list
    del xy_coordinates[len(xy_coordinates)-2]
    del xy_coordinates[len(xy_coordinates)-1]

    # Condition to check if 2 adjacent points are separated by more than 100 meters
    # If yes, insert a discretize to 20 meter points in between

    new_coordinates = []
    for i in range(len(xy_coordinates) - 1):
        x1 = xy_coordinates[i][0]
        y1 = xy_coordinates[i][1]
        x2 = xy_coordinates[i + 1][0]
        y2 = xy_coordinates[i + 1][1]

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

    new_coordinates.append(xy_coordinates[-1])

    #Route slopes also
    slopeangle_list = []

    for i in range(len(new_coordinates) - 1):
        x1 = new_coordinates[i][0]
        y1 = new_coordinates[i][1]
        x2 = new_coordinates[i + 1][0]
        y2 = new_coordinates[i + 1][1]

        distance_x = abs(x2 - x1)
        distance_y = abs(y2 - y1)

        if distance_x == 0:
            slopeangle_list.append(np.pi / 2)
        else:
            slopeangle_list.append(math.atan(distance_y / distance_x))

    slopeangle_list.append(slopeangle_list[-1])

    return new_coordinates, slopeangle_list


# Write to a csv file
def write_to_csv(xy_coordinates, slopeangle_list):
    with open('Routenew.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['X', 'Y', 'SlopeAngle'])
        for i in range(len(xy_coordinates)):
            writer.writerow([xy_coordinates[i][0], xy_coordinates[i][1], slopeangle_list[i]])


# Test
xy_coordinates, slopeangle_list= dumfunc()
write_to_csv(xy_coordinates, slopeangle_list)

#Plot the route
import matplotlib.pyplot as plt
x = []
y = []
for i in range(len(xy_coordinates)):
    x.append(xy_coordinates[i][0])
    y.append(xy_coordinates[i][1])
plt.plot(x, y)
#Axes labels
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Route')
plt.show()