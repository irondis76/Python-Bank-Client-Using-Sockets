# Simple Banking System

This is a simple banking system implemented in Python using socket programming. The system consists of a server and a client application that communicate over a secure SSL/TLS connection.

## Introduction

The banking system allows users to perform basic banking operations such as login, checking balance, withdrawing, and depositing money. User data is stored in a CSV file, and the server handles client requests to perform these operations.

## How to Run

### Server
1. Clone the repository to your local machine.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Generate SSL certificate and key files using OpenSSL: openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt -subj "/C=IN/ST=Karnataka/L=Bengaluru/O=XYZ Bank/OU=BANK/CN=XYZ Bank Server/emailAddress=xyzbankadmin@gmail.com" -addext "subjectAltName=<YOURIPADDRESS>"
4. Run the server: `python server.py`

### Client
1. Run the client: `python client.py`

## How It Works

- The server listens for incoming connections from clients on a specified IP address and port.
- Upon connection, the client and server establish a secure SSL/TLS connection.
- The client can send requests to the server to perform banking operations such as login, checking balance, withdrawing, and depositing money.
- The server validates the requests, performs the requested operation, and sends back a response to the client.
- User data is stored in a CSV file on the server, and the server reads from and writes to this file to manage user accounts and balances.

## Contributors

- [Dishanth.K](https://github.com/irondis76)



