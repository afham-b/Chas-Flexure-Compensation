import socket


def cleanup():
    server_address = ('127.0.0.1', 5001)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(server_address)
        print("Socket closed")
    except OSError as e:
        print(f"Socket bind failed: {e}")
    finally:
        sock.close()


if __name__ == "__main__":
    cleanup()
