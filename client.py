import socket
import ssl
from tkinter import simpledialog, messagebox
from customtkinter import *

HOST = '192.168.1.210'
PORT = 12345
CERT_FILE = 'server.crt'

class BankClient(CTk):
    def __init__(self):
        super().__init__()

        set_default_color_theme("green")

        self.title("Bank Client")

        title_label = CTkLabel(self, text="XYZ Bank",
                               font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        self.dynamic_label = CTkLabel(self, text="Hello Customer, Welcome to XYZ Bank", font=(
            "Arial", 20), text_color="#FFCC70")
        self.dynamic_label.pack(pady=10)

        login_title_label = CTkLabel(
            self, text="Login", font=("Helvetica", 14, "bold"))
        login_title_label.pack(pady=5)

        self.label_name = CTkLabel(self, text="Name:")
        self.entry_name = CTkEntry(self)
        self.label_pin = CTkLabel(self, text="PIN:")
        self.entry_pin = CTkEntry(self, show="*")

        self.label_name.pack()
        self.entry_name.pack()
        self.label_pin.pack()
        self.entry_pin.pack()

        self.login_button = CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        operations_title_label = CTkLabel(
            self, text="Operations", font=("Helvetica", 14, "bold"))
        operations_title_label.pack(pady=10)

        self.balance_button = CTkButton(
            self, text="Check Balance", command=self.check_balance)
        self.balance_button.pack(pady=5)

        self.withdraw_button = CTkButton(
            self, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack(pady=5)

        self.deposit_button = CTkButton(
            self, text="Deposit", command=self.deposit)
        self.deposit_button.pack(pady=5)

        self.response_label = CTkLabel(self, text="")
        self.response_label.pack(pady=10)

        # Create SSL context with the self-signed certificate
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.load_verify_locations(CERT_FILE)

        # Create socket and wrap it with SSL
        self.socket = self.context.wrap_socket(socket.socket(
            socket.AF_INET, socket.SOCK_STREAM), server_hostname=HOST)
        self.socket.connect((HOST, PORT))

        print("SSL Version:", self.socket.version())
        print("Cipher:", self.socket.cipher())
        print("Server Certificate:")
        try:
            cert = self.socket.getpeercert()
            if cert:
                print("Server Certificate:")
                for key, value in cert.items():
                    print(key, ":", value)
            else:
                print("No server certificate found.")
        except ssl.SSLError as e:
            print("Error retrieving server certificate:", e)

    def send_message(self, message):
        try:
            print(f"Sending message: {message}")
            self.socket.sendall(message.encode())
            response = self.socket.recv(1024).decode()
            print(f"Received response: {response}")
            self.response_label.configure(text=response)
        except socket.error as e:
            messagebox.showerror("Error", f"Socket error: {e}")

    def login(self):
        name = self.entry_name.get()
        pin = self.entry_pin.get()
        message = f"login {name} {pin}"
        self.send_message(message)

    def check_balance(self):
        name = self.entry_name.get()
        message = f"balance {name}"
        self.send_message(message)

    def withdraw(self):
        name = self.entry_name.get()
        amount = self.ask_amount()
        if amount is not None:
            message = f"withdraw {name} {amount}"
            self.send_message(message)

    def deposit(self):
        name = self.entry_name.get()
        amount = self.ask_amount()
        if amount is not None:
            message = f"deposit {name} {amount}"
            self.send_message(message)

    def ask_amount(self):
        try:
            amount = simpledialog.askinteger("Amount", "Enter amount:")
            if amount is None:
                return None
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return None
            return amount
        except ValueError:
            messagebox.showerror(
                "Error", "Invalid input. Please enter a valid integer.")
            return None

if __name__ == "__main__":
    app = BankClient()
    app.mainloop()
