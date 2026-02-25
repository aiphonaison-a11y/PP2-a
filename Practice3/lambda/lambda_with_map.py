if __name__ == "__main__":
    # Example 1: convert temperatures with map + lambda
    celsius_values = [0, 10, 20, 37]
    fahrenheit_values = list(map(lambda c: (c * 9/5) + 32, celsius_values))
    print("Celsius:", celsius_values)
    print("Fahrenheit:", [round(x, 1) for x in fahrenheit_values])

    # Example 2: normalize names (strip + title-case)
    raw_names = ["  aLiYa ", "dANA", "   amina"]
    clean_names = list(map(lambda n: n.strip().title(), raw_names))
    print("Clean names:", clean_names)

    # Example 3: extract fields from dictionaries
    students = [
        {"name": "Amina", "score": 18},
        {"name": "Dana", "score": 20},
        {"name": "Aliya", "score": 17},
    ]
    scores = list(map(lambda s: s["score"], students))
    print("Scores:", scores)

    # Example 4: apply tax/fee calculation
    prices = [1200, 2500, 8000]
    final_prices = list(map(lambda p: round(p * 1.12, 2), prices))  # 12% tax
    print("Final prices (12% tax):", final_prices)
