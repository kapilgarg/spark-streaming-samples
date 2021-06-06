"""
TCP server
"""
import socket
import time
import order


HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 9998        # Port to listen on (non-privileged ports are > 1023)
DELAY = 0.01

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('connected to', addr)
        while True:
            message = order.generate_order()
            conn.sendall(bytes(message, 'utf-8'))
            time.sleep(DELAY)
