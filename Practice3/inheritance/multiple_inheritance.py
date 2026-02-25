class CanRun:
    def run(self) -> str:
        return "Running..."


class CanSwim:
    def swim(self) -> str:
        return "Swimming..."


class Athlete(CanRun, CanSwim):
    def __init__(self, name: str):
        self.name = name

    def intro(self) -> str:
        return f"Athlete: {self.name}"


# Demonstrate MRO with two parents that share the same method name
class A:
    def who(self) -> str:
        return "A"


class B:
    def who(self) -> str:
        return "B"


class C(A, B):
    pass


class D(B, A):
    pass


if __name__ == "__main__":
    # Example 1: athlete has both abilities
    a = Athlete("Amina")
    print(a.intro())
    print(a.run())
    print(a.swim())

    # Example 2: MRO decides which parent method is used first
    print("C MRO:", [cls.__name__ for cls in C.mro()])
    print("C.who():", C().who())  # A comes before B in class definition

    print("D MRO:", [cls.__name__ for cls in D.mro()])
    print("D.who():", D().who())  # B comes before A in class definition
