# eci_to_ecef.py
#
# Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km
# python3 eci_to_ecef.py 2054 4 29 11 29 3.3 5870.038832 3389.068500 3838.027968
# Converts from ECI to ECEF.
#
# Parameters:
# year XXXX
# month XX
# day XX
# hour XX
# minute XX
# second XX.XX
# eci_x_km
# eci_y_km
# eci_z_km
# Output:
# ecef_x_km
# ecef_y_km
# ecef_z_km

# Written By: Samuel Jacobson

import sys
import math

# Parse script arguments
if len(sys.argv) == 10:
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    hour = int(sys.argv[4])
    minute = int(sys.argv[5])
    second = float(sys.argv[6])
    eci_x_km = float(sys.argv[7])
    eci_y_km = float(sys.argv[8])
    eci_z_km = float(sys.argv[9])
else:
    print('Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km')
    exit()

# Julian Date calculation
def ymdhms_to_jd(year, month, day, hour, minute, second):
    # Convert time to fractional day
    day_fraction = (hour + minute / 60 + second / 3600) / 24.0

    # Adjust year and month for the algorithm
    if month <= 2:
        year -= 1
        month += 12

    # Integer division
    A = year // 100
    B = 2 - A + (A // 4)

    # Julian Date
    jd = int(365.25 * (year + 4716)) \
         + int(30.6001 * (month + 1)) \
         + day + day_fraction + B - 1524.5

    return jd

def multiply_matrix_vector(rotation_matrix, vector):
    result = [[0], [0], [0]]  # Initialize a 3x1 result vector
    for i in range(3):
        for j in range(3):
            result[i][0] += rotation_matrix[i][j] * vector[j][0]
    return result

# Calculating GMST angle
jd_frac = ymdhms_to_jd(year, month, day, hour, minute, second)
Tuti = (jd_frac - 2451545) / 36525
GMST = (67310.54841 + (876600 * 60 * 60 + 8640184.812866) *
        Tuti + 0.093104 * Tuti ** 2 + (-6.2 * 10 ** -6) * Tuti ** 3)
gmst = GMST % 86400
GMST_rad = gmst * (7.292115*10**-5)


# Rotation matrix for ECI to ECEF
rotation_matrix = [
    [math.cos(-GMST_rad),  -math.sin(-GMST_rad), 0],
    [math.sin(-GMST_rad), math.cos(-GMST_rad), 0],
    [0,                   0,                  1]
]

# ECI vector
eci_vector = [
    [eci_x_km],
    [eci_y_km],
    [eci_z_km]
]

# Perform the rotation to get ECEF coordinates
ecef_vector = multiply_matrix_vector(rotation_matrix, eci_vector)

# Extract ECEF coordinates
ecef_x_km = ecef_vector[0][0]
ecef_y_km = ecef_vector[1][0]
ecef_z_km = ecef_vector[2][0]


# Print results

print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)
