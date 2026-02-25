class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = float(width)
        self.height = float(height)

    def area(self) -> float:
        return self.width * self.height

    @classmethod
    def from_square(cls, side: float) -> "Rectangle":
        """Alternate constructor: creates a square rectangle."""
        return cls(side, side)

    @staticmethod
    def is_positive(number: float) -> bool:
        """Utility: doesn't use self or cls."""
        return number > 0


if __name__ == "__main__":
    # Example 1: regular constructor
    r1 = Rectangle(3, 4)
    print("r1 area:", r1.area())

    # Example 2: classmethod as alternate constructor
    square = Rectangle.from_square(5)
    print("square area:", square.area())

    # Example 3: staticmethod utility usage
    print("is_positive(10):", Rectangle.is_positive(10))
    print("is_positive(-2):", Rectangle.is_positive(-2))

    # Example 4: instance methods operate on instance state
    r1.width = 10
    print("r1 new area after width change:", r1.area())
