class Person:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Student(Person):
    def __init__(self, first_name: str, last_name: str, grade: int):
        # super() calls the parent constructor so we don't repeat code
        super().__init__(first_name, last_name)
        self.grade = grade

    def full_name(self) -> str:
        # extend parent method by calling super().full_name()
        return f"{super().full_name()} (Grade {self.grade})"


if __name__ == "__main__":
    # Example 1: parent instance
    p = Person("Amina", "Khan")
    print(p.full_name())

    # Example 2: child instance uses super() to set shared attributes
    s = Student("Dana", "Nur", grade=11)
    print(s.full_name())

    # Example 3: verify inherited attributes exist
    print("Student first name:", s.first_name)
