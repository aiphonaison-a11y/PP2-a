from functools import reduce

nums = [1, 2, 3, 4, 5]

# map()
squares = list(map(lambda x: x**2, nums))
print(squares)

# filter()
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)

# reduce() sum
total = reduce(lambda x, y: x + y, nums)
print(total)

# reduce() product
product = reduce(lambda x, y: x * y, nums)
print(product)