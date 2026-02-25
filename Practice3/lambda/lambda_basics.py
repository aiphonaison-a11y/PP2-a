# Regular function (named)
def square(x: int) -> int:
    return x * x


if __name__ == "__main__":
    # Example 1: lambda equivalent of a simple named function
    square_lambda = lambda x: x * x  # noqa: E731 (allowed for practice)
    print("square(5):", square(5))
    print("square_lambda(5):", square_lambda(5))

    # Example 2: lambda with multiple parameters
    area = lambda w, h: w * h  # noqa: E731
    print("area(3, 4):", area(3, 4))

    # Example 3: lambda as a quick key function
    words = ["banana", "fig", "apple", "kiwi"]
    print("Sorted by length:", sorted(words, key=lambda s: len(s)))

    # Example 4: choosing between lambda and def
    # Use def when logic grows (multiple lines / checks / clarity)
    def safe_title(text: str) -> str:
        if not text.strip():
            return "(empty)"
        return text.strip().title()

    # Use lambda when it's a short expression
    trim = lambda s: s.strip()  # noqa: E731

    print("safe_title('  hello  '):", safe_title("  hello  "))
    print("trim('  hello  '):", trim("  hello  "))
