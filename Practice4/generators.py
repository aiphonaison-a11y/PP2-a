# generators.py

# This function creates a generator.
# It gives the square of each number from 0 up to n.
def square_generator(n):
    # range(n + 1) means numbers from 0 to n inclusive
    for i in range(n + 1):
        # yield sends one value at a time
        yield i * i


# Print a title so the output is easier to read
print("1. Squares up to N:")

# Store a sample number in n1
n1 = 5

# Loop through the generator values
for value in square_generator(n1):
    print(value)


# This function generates even numbers from 0 to n
def even_numbers(n):
    # Start from 0, go to n, step by 2
    for i in range(0, n + 1, 2):
        yield i


# Print a title
print("\n2. Even numbers from 0 to n:")

# Ask the user to enter n
n2 = int(input("Enter n: "))

# Convert each generated number to string and join with commas
print(",".join(str(num) for num in even_numbers(n2)))


# This function generates numbers divisible by both 3 and 4
def divisible_by_3_and_4(n):
    # Check every number from 0 to n
    for i in range(n + 1):
        # If number is divisible by 3 and by 4
        if i % 3 == 0 and i % 4 == 0:
            yield i


# Print a title
print("\n3. Numbers divisible by 3 and 4:")

# Ask the user for n
n3 = int(input("Enter n: "))

# Print each matching number
for num in divisible_by_3_and_4(n3):
    print(num)


# This function generates squares from a to b
def squares(a, b):
    # Loop from a to b inclusive
    for i in range(a, b + 1):
        yield i * i


# Print a title
print("\n4. Squares from a to b:")

# Ask for starting number
a = int(input("Enter a: "))

# Ask for ending number
b = int(input("Enter b: "))

# Print each square
for value in squares(a, b):
    print(value)


# This function counts down from n to 0
def countdown(n):
    # Repeat while n is not less than 0
    while n >= 0:
        yield n
        n -= 1


# Print a title
print("\n5. Countdown from n to 0:")

# Ask for n
n5 = int(input("Enter n: "))

# Print all countdown values
for num in countdown(n5):
    print(num)