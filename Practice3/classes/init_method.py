class BankAccount:
    """A simple bank account example."""

    def __init__(self, owner: str, balance: float = 0.0):
        # validation inside __init__
        if balance < 0:
            raise ValueError("Starting balance cannot be negative.")
        self.owner = owner
        self.balance = float(balance)

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive.")
        self.balance += amount

    def withdraw(self, amount: float) -> bool:
        """Tries to withdraw; returns True if successful."""
        if amount <= 0:
            return False
        if amount > self.balance:
            return False
        self.balance -= amount
        return True


if __name__ == "__main__":
    # Example 1: default balance
    acc1 = BankAccount("Amina")
    print(acc1.owner, "balance:", acc1.balance)

    # Example 2: custom starting balance
    acc2 = BankAccount("Dana", balance=15000)
    print(acc2.owner, "balance:", acc2.balance)

    # Example 3: update state via methods
    acc2.deposit(2500)
    print("After deposit:", acc2.balance)

    # Example 4: constructor validation demo (wrapped so the script doesn't crash)
    try:
        bad = BankAccount("Test", balance=-5)
    except ValueError as e:
        print("Validation works:", e)
