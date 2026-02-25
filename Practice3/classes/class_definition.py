class Student:
    """Represents a student with a name and scores."""

    def __init__(self, name: str):
        self.name = name
        self.scores: list[int] = []

    def add_score(self, score: int) -> None:
        """Adds a score to the student's list."""
        self.scores.append(score)

    def average_score(self) -> float:
        """Returns average score (0 if no scores)."""
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)

    def __str__(self) -> str:
        return f"Student(name={self.name}, avg={self.average_score():.2f})"


if __name__ == "__main__":
    # Example 1: create objects
    amina = Student("Amina")
    dana = Student("Dana")

    # Example 2: set and use attributes through methods
    amina.add_score(18)
    amina.add_score(20)

    dana.add_score(17)
    dana.add_score(19)

    # Example 3: call instance methods
    print(amina.name, "avg:", amina.average_score())
    print(dana.name, "avg:", dana.average_score())

    # Example 4: __str__ helps print objects nicely
    print("Object printing:", amina)
