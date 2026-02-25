def greet(name: str) -> None:
    """Prints a greeting message."""
    print(f"Hello, {name}!")


def format_full_name(first_name: str, last_name: str) -> str:
    """Returns a nicely formatted full name."""
    return f"{first_name.strip().title()} {last_name.strip().title()}"


def celsius_to_fahrenheit(celsius: float) -> float:
    """Converts Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32


def is_even(number: int) -> bool:
    """Returns True if number is even, otherwise False."""
    return number % 2 == 0


if __name__ == "__main__":
    # Example 1: Basic function call
    greet("Amina")
    greet("Dana")

    # Example 2: Function returning a value
    full_name = format_full_name("  aLiYa  ", "  nUr  ")
    print("Formatted name:", full_name)

    # Example 3: Reusable numeric helper
    for c in [0, 20, 37]:
        f = celsius_to_fahrenheit(c)
        print(f"{c}°C = {f:.1f}°F")

    # Example 4: Boolean-returning function used in logic
    numbers = [3, 4, 10, 11]
    evens = [n for n in numbers if is_even(n)]
    print("Even numbers:", evens)
