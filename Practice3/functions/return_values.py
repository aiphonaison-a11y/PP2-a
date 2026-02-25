def safe_divide(a: float, b: float) -> float | None:
    """Returns a/b, or None if division is not possible."""
    if b == 0:
        return None
    return a / b


def first_non_empty(values: list[str]) -> str:
    """Returns the first non-empty string, or an empty string if none found."""
    for v in values:
        if v.strip():
            return v.strip()  # early return (stop as soon as we find a good value)
    return ""


def min_max(numbers: list[int]) -> tuple[int, int] | None:
    """Returns (min, max) as a tuple, or None for empty lists."""
    if not numbers:
        return None
    return min(numbers), max(numbers)


def validate_password(password: str) -> tuple[bool, str]:
    """Returns (is_valid, message) to explain validation result."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if password.lower() == password or password.upper() == password:
        return False, "Password must contain both uppercase and lowercase letters."
    if not any(ch.isdigit() for ch in password):
        return False, "Password must include at least one digit."
    return True, "Password looks good."


if __name__ == "__main__":
    # Example 1: None as 'no result'
    result = safe_divide(10, 0)
    print("10 / 0 =>", result)

    # Example 2: early return from a loop
    candidates = ["", "   ", "First real value", "Another"]
    print("First non-empty:", first_non_empty(candidates))

    # Example 3: returning multiple values as a tuple
    data = [5, 1, 9, 3]
    extremes = min_max(data)
    if extremes:
        smallest, largest = extremes
        print("Min:", smallest, "Max:", largest)

    # Example 4: status + message return pattern
    for pwd in ["short", "alllowercase9", "GoodPass9"]:
        ok, message = validate_password(pwd)
        print(f"{pwd!r} => valid={ok} | {message}")
