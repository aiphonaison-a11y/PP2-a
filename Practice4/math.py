# math.py

# Import the math module
import math


# 1. Convert degree to radian

# Ask the user to enter the degree
degree = int(input("Input degree: "))

# Convert degree to radian using the formula
radian = degree * (math.pi / 180)

# Print the result rounded to 6 decimal places
print("Output radian:", round(radian, 6))


# 2. Calculate the area of a trapezoid

# Ask the user for the height
height = float(input("\nHeight: "))

# Ask for the first base
base1 = float(input("Base, first value: "))

# Ask for the second base
base2 = float(input("Base, second value: "))

# Use the trapezoid area formula
trapezoid_area = ((base1 + base2) * height) / 2

# Print the result
print("Expected Output:", trapezoid_area)


# 3. Calculate the area of a regular polygon

# Ask for number of sides
sides = int(input("\nInput number of sides: "))

# Ask for side length
side_length = float(input("Input the length of a side: "))

# Use the regular polygon area formula
polygon_area = (sides * side_length ** 2) / (4 * math.tan(math.pi / sides))

# Print the area
print("The area of the polygon is:", round(polygon_area, 0))


# 4. Calculate the area of a parallelogram

# Ask for base length
base = float(input("\nLength of base: "))

# Ask for height
height_p = float(input("Height of parallelogram: "))

# Formula: area = base * height
parallelogram_area = base * height_p

# Print the result
print("Expected Output:", parallelogram_area)