if __name__ == "__main__":
    # Example 1: sort tuples by second value (score)
    results = [("Amina", 18), ("Dana", 20), ("Aliya", 17)]
    by_score = sorted(results, key=lambda t: t[1], reverse=True)
    print("Sorted by score (desc):", by_score)

    # Example 2: sort dictionaries by a field
    books = [
        {"title": "Python Basics", "pages": 220},
        {"title": "Data Science", "pages": 540},
        {"title": "Algorithms", "pages": 410},
    ]
    by_pages = sorted(books, key=lambda b: b["pages"])
    print("Sorted by pages:", [(b["title"], b["pages"]) for b in by_pages])

    # Example 3: sort strings by last character
    words = ["bake", "dance", "code", "smile"]
    by_last_char = sorted(words, key=lambda w: w[-1])
    print("Sorted by last char:", by_last_char)

    # Example 4: custom sort for dates stored as strings (YYYY-MM-DD)
    # Sorting works because the format is already chronological.
    dates = ["2026-02-01", "2025-11-30", "2026-01-15"]
    print("Sorted dates:", sorted(dates, key=lambda d: d))
