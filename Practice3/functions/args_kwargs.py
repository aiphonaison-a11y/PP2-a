def add_all(*numbers: float) -> float:
    """Sums any amount of numbers."""
    return sum(numbers)


def build_message(template: str, **fields) -> str:
    """Formats a template using keyword fields.

    Example:
        build_message("Hello {name}", name="Amina") -> "Hello Amina"
    """
    return template.format(**fields)


def debug_print(*values, sep: str = " ", end: str = "\n", **metadata) -> None:
    """A tiny 'logger' that accepts flexible values + metadata."""
    prefix = " ".join(f"{k}={v}" for k, v in metadata.items())
    if prefix:
        prefix = "[" + prefix + "] "
    print(prefix + sep.join(str(v) for v in values), end=end)


def apply_discount(price: float, **options) -> float:
    """Applies discounts controlled by keyword-only options.

    Supported options:
    - percent: e.g. 10 means 10% off
    - fixed: fixed amount off
    """
    percent = float(options.get("percent", 0))
    fixed = float(options.get("fixed", 0))
    discounted = price * (1 - percent / 100) - fixed
    return max(discounted, 0.0)  # never go below 0


if __name__ == "__main__":
    # Example 1: *args to accept many numbers
    print("Add 1,2,3 =>", add_all(1, 2, 3))
    print("Add many =>", add_all(2.5, 10, 1.5, 6))

    # Example 2: **kwargs to format a message
    msg = build_message("Order for {name}: {count} items", name="Amina", count=4)
    print(msg)

    # Example 3: mix *args with named parameters and extra metadata
    debug_print("Starting...", 2026, sep=" | ", module="args_kwargs", level="INFO")

    # Example 4: practical **kwargs configuration
    original = 12500
    print("Original:", original)
    print("10% off:", apply_discount(original, percent=10))
    print("10% off + 500 fixed:", apply_discount(original, percent=10, fixed=500))
