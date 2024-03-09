import socket
import ssl
import threading
import csv

users = {}  

HOST = '192.168.1.210'
PORT = 12345
CSV_FILE = 'users.csv'


def load_user_data():
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row.get('name')
            pin = row.get('pin', '')  
            balance = float(row.get('balance', 0))  
            users[name] = {'pin': pin, 'balance': balance}

def save_user_data():
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'pin', 'balance'])
        writer.writeheader()
        for name, data in users.items():
            writer.writerow({'name': name, 'pin': data['pin'], 'balance': data['balance']})

def authenticate_user(name, pin):
    if name in users:
        if users[name]["pin"] == pin:
            return True
    return False

def handle_client(conn, addr):
    print(f"Connected to {addr}")

    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode()
            parts = message.split()
            command = parts[0]

            if command == "login":
                name = parts[1]
                pin = parts[2]
                if authenticate_user(name, pin):
                    response = f"Welcome, {name}!"
                else:
                    response = "Invalid name or PIN"
            elif command == "balance":
                name = parts[1]
                if name in users:
                    response = f"Your balance is Rs.{users[name]['balance']}"
                else:
                    response = "User not found"
            elif command == "withdraw":
                name = parts[1]
                amount = float(parts[2])
                if name in users:
                    if amount <= users[name]["balance"]:
                        users[name]["balance"] -= amount
                        save_user_data()  
                        response = f"Withdrawn Rs.{amount}. Your balance is now Rs.{users[name]['balance']}"
                    else:
                        response = "Insufficient funds"
                else:
                    response = "User not found"
            elif command == "deposit":
                name = parts[1]
                amount = float(parts[2])
                if name in users:
                    users[name]["balance"] += amount
                    save_user_data()  
                    response = f"Deposited Rs.{amount}. Your balance is now Rs.{users[name]['balance']}"
                else:
                    response = "User not found"
            else:
                response = "Invalid request"

            conn.sendall(response.encode())


load_user_data()  

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Bank server is listening...")
    with context.wrap_socket(server_socket, server_side=True) as secure_socket:
        while True:
            conn, addr = secure_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
