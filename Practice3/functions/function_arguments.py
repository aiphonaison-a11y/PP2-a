def order_summary(item: str, quantity: int, price_per_item: float) -> str:
    """Creates a short summary for a simple order."""
    total = quantity * price_per_item
    return f"{quantity} x {item} => {total:.2f} KZT"


def build_username(first_name: str, last_name: str, year: int = 2026) -> str:
    """Creates a username; year is optional (default argument)."""
    return f"{first_name.lower()}.{last_name.lower()}{year}"


def average(scores: list[float]) -> float:
    """Returns average of a list of numbers (list passed as argument)."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def describe_student(profile: dict) -> str:
    """Shows passing a dictionary (any data type can be passed)."""
    name = profile.get("name", "Unknown")
    grade = profile.get("grade", "?")
    interests = ", ".join(profile.get("interests", [])) or "(none)"
    return f"Student: {name} | Grade: {grade} | Interests: {interests}"


if __name__ == "__main__":
    # Example 1: Positional arguments
    print(order_summary("Notebook", 3, 450.0))

    # Example 2: Keyword arguments (order doesn't matter)
    print(order_summary(price_per_item=1200.0, item="Pen set", quantity=2))

    # Example 3: Default argument used vs overridden
    print("Default year:", build_username("Amina", "Khan"))
    print("Custom year:", build_username("Amina", "Khan", year=2024))

    # Example 4: Passing a list (scores)
    mock_scores = [18, 19, 17, 20]
    print("Average score:", average(mock_scores))

    # Example 5: Passing a dict
    profile = {"name": "Amina", "grade": 11, "interests": ["astronomy", "dance"]}
    print(describe_student(profile))
