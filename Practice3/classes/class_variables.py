class Device:
    # Class variable (shared across all instances unless shadowed)
    category = "electronics"

    def __init__(self, name: str, price: float):
        # Instance variables (unique per object)
        self.name = name
        self.price = float(price)

    def __repr__(self) -> str:
        return f"Device(name={self.name!r}, price={self.price}, category={self.category!r})"


if __name__ == "__main__":
    # Example 1: two instances share the same class variable
    phone = Device("Phone", 120000)
    laptop = Device("Laptop", 450000)
    print("Initial:", phone, laptop)

    # Example 2: change class variable affects all instances (that don't override it)
    Device.category = "tech"
    print("After changing Device.category:", phone, laptop)

    # Example 3: override category only for one instance (creates an instance attribute)
    phone.category = "mobile"  # now phone has its OWN 'category'
    print("After overriding phone.category:", phone, laptop)

    # Example 4: modifying and deleting object properties
    laptop.price = 430000  # modify
    print("Laptop updated price:", laptop)

    del laptop.name  # delete attribute
    # Check with hasattr to avoid AttributeError
    print("Laptop has name?", hasattr(laptop, "name"))
