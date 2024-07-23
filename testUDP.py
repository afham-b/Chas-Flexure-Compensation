# checking connection

import socket

def send_test_data():
    test_data = '1.0,1.0'  # Simulate some realistic test data
    pico_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 5001)
    pico_sock.sendto(test_data.encode(), server_address)
    print("Test data sent:", test_data)

send_test_data()