#Ex1
print(bool("Hello"))
print(bool(15))

#Ex2
x = "Hello"
y = 15

print(bool(x))
print(bool(y))

#Ex3
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#Ex4
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

#Ex5
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))  # False
