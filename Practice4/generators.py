
# 1. Using iter() and next()

numbers = [10, 20, 30]
iterator = iter(numbers)

print("Using iter() and next():")
print(next(iterator))
print(next(iterator))
print(next(iterator))



# 2. Custom Iterator Class

class CountUpTo:
    def __init__(self, limit):
        self.limit = limit
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.limit:
            value = self.current
            self.current += 1
            return value
        else:
            raise StopIteration


print("\nCustom Iterator:")
counter = CountUpTo(5)
for number in counter:
    print(number)




# 3. Generator Function

def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i


print("\nGenerator Function (even numbers):")
for num in even_numbers(10):
    print(num)




# 4. Generator Expression

print("\nGenerator Expression (squares):")
squares = (x * x for x in range(5))
for square in squares:
    print(square)