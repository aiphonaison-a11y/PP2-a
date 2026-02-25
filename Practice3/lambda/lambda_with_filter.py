if __name__ == "__main__":
    # Example 1: filter even numbers
    numbers = list(range(1, 16))
    evens = list(filter(lambda n: n % 2 == 0, numbers))
    print("Numbers:", numbers)
    print("Evens:", evens)

    # Example 2: filter strings longer than 4
    words = ["sun", "planet", "star", "galaxy", "sky"]
    long_words = list(filter(lambda w: len(w) > 4, words))
    print("Long words:", long_words)

    # Example 3: filter passing scores
    scores = [10, 14, 18, 9, 20, 12]
    passing = list(filter(lambda s: s >= 14, scores))
    print("Passing (>=14):", passing)

    # Example 4: filter dictionaries by condition
    products = [
        {"name": "Keyboard", "price": 9500, "in_stock": True},
        {"name": "Mouse", "price": 4500, "in_stock": False},
        {"name": "Headset", "price": 12000, "in_stock": True},
    ]
    available = list(filter(lambda p: p["in_stock"], products))
    affordable = list(filter(lambda p: p["price"] <= 10000, products))
    print("Available:", [p["name"] for p in available])
    print("Affordable (<=10000):", [p["name"] for p in affordable])
