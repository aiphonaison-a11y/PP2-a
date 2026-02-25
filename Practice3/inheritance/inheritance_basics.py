class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "(silent)"


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


if __name__ == "__main__":
    # Example 1: base class usage
    mystery = Animal("Mystery")
    print(mystery.name, "says", mystery.speak())

    # Example 2: child classes inherit 'name' and override behavior
    dog = Dog("Rex")
    cat = Cat("Luna")
    print(dog.name, "says", dog.speak())
    print(cat.name, "says", cat.speak())

    # Example 3: polymorphism (same method name, different results)
    animals: list[Animal] = [mystery, dog, cat]
    for a in animals:
        print(f"{a.name}: {a.speak()}")
