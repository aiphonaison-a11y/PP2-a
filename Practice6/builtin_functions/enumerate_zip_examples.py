names = ["Ali", "Aru", "Dana"]
scores = [90, 85, 88]

# numerate()
for i, name in enumerate(names):
    print(i, name)

# enumerate with start index
for i, name in enumerate(names, start=1):
    print(i, name)

# zip()
for name, score in zip(names, scores):
    print(name, score)

# type conversion and checking
x = "123"
print(type(x))
x = int(x)
print(type(x))

y = 45
print(str(y))