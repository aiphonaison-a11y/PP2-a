import math
import random


# 1. Built-in Math Functions

print("Min:", min(3, 7, 1))
print("Max:", max(3, 7, 1))
print("Absolute:", abs(-15))
print("Round:", round(3.14159, 2))
print("Power:", pow(2, 4))



# 2. math Module

print("Square Root:", math.sqrt(25))
print("Ceiling:", math.ceil(4.3))
print("Floor:", math.floor(4.8))
print("Pi:", math.pi)
print("Euler's number:", math.e)


# 3. random Module

print("Random float:", random.random())
print("Random integer (1-10):", random.randint(1, 10))
print("Random choice:", random.choice(["apple", "banana", "cherry"]))

numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print("Shuffled list:", numbers)