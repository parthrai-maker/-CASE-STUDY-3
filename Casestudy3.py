from abc import ABC, abstractmethod

# ------------------ Abstract Base Class ------------------
class Payment(ABC):
    def __init__(self, user_name):
        self.user_name = user_name
        self.original_amount = 0
        self.final_amount = 0

    @abstractmethod
    def pay(self, amount):
        pass

    def generate_receipt(self):
        print("\n----- PAYMENT RECEIPT -----")
        print(f"User Name       : {self.user_name}")
        print(f"Original Amount : ₹{self.original_amount:.2f}")
        print(f"Final Amount    : ₹{self.final_amount:.2f}")
        print("----------------------------")


# ------------------ Credit Card ------------------
class CreditCardPayment(Payment):
    def pay(self, amount):
        self.original_amount = amount
        
        gateway_fee = 0.02 * amount
        gst = 0.18 * gateway_fee
        
        self.final_amount = amount + gateway_fee + gst
        
        print("\nProcessing Credit Card Payment...")
        print(f"Gateway Fee: ₹{gateway_fee:.2f}")
        print(f"GST on Fee: ₹{gst:.2f}")
        
        return self.final_amount


# ------------------ UPI ------------------
class UPIPayment(Payment):
    def pay(self, amount):
        self.original_amount = amount
        
        cashback = 50 if amount > 1000 else 0
        self.final_amount = amount - cashback
        
        print("\nProcessing UPI Payment...")
        print(f"Cashback: ₹{cashback}")
        
        return self.final_amount


# ------------------ PayPal ------------------
class PayPalPayment(Payment):
    def pay(self, amount):
        self.original_amount = amount
        
        fee = 0.03 * amount
        conversion_fee = 20
        
        self.final_amount = amount + fee + conversion_fee
        
        print("\nProcessing PayPal Payment...")
        print(f"Transaction Fee: ₹{fee:.2f}")
        print(f"Conversion Fee: ₹{conversion_fee}")
        
        return self.final_amount


# ------------------ Wallet ------------------
class WalletPayment(Payment):
    def __init__(self, user_name, balance):
        super().__init__(user_name)
        self.balance = balance

    def pay(self, amount):
        self.original_amount = amount
        
        print("\nProcessing Wallet Payment...")
        
        if amount > self.balance:
            print("❌ Transaction Failed: Insufficient Balance")
            self.final_amount = 0
            return None
        
        self.balance -= amount
        self.final_amount = amount
        
        print(f"Remaining Balance: ₹{self.balance:.2f}")
        return self.final_amount


# ------------------ Process Function ------------------
def process_payment(payment, amount):
    result = payment.pay(amount)
    
    if result is not None:
        payment.generate_receipt()
    else:
        print("Payment could not be completed.")


# ------------------ Main Menu ------------------
if __name__ == "__main__":
    user = input("Enter your name: ")
    wallet_balance = float(input("Enter initial wallet balance: ₹"))

    wallet = WalletPayment(user, wallet_balance)

    while True:
        print("\n====== PAYMENT MENU ======")
        print("1. Credit Card")
        print("2. UPI")
        print("3. PayPal")
        print("4. Wallet")
        print("5. Exit")

        choice = int(input("Enter your choice: "))
        
        if choice == 5:
            print("Exiting... Thank you!")
            break

        amount = float(input("Enter amount to pay: ₹"))

        if choice == 1:
            payment = CreditCardPayment(user)
        elif choice == 2:
            payment = UPIPayment(user)
        elif choice == 3:
            payment = PayPalPayment(user)
        elif choice == 4:
            payment = wallet   # same wallet object (balance updates)
        else:
            print("Invalid choice! Try again.")
            continue

        process_payment(payment, amount)