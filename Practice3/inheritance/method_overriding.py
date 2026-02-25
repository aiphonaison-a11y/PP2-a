class Notification:
    def send(self, message: str) -> None:
        print(f"[Notification] {message}")


class EmailNotification(Notification):
    def send(self, message: str) -> None:
        # override: change format + extend behavior
        print("Connecting to email server...")
        super().send(f"EMAIL: {message}")  # call parent version
        print("Email sent.")


class SMSNotification(Notification):
    def send(self, message: str) -> None:
        # override without calling super (fully custom behavior)
        print(f"[SMS] {message}")


if __name__ == "__main__":
    # Example 1: base behavior
    base = Notification()
    base.send("Hello!")

    # Example 2: overridden + super()
    email = EmailNotification()
    email.send("Your code is ready.")

    # Example 3: overridden without super()
    sms = SMSNotification()
    sms.send("Meet at 6.")
