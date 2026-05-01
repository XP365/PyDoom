import socket
import threading

def SendPacket(sock, data):
    # REMOVED the while True loop here
    try:
        sock.send(data.encode('utf-8'))
    except:
        print("Failed to send message.")



def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                break
            # Just printing the raw data for clarity
            thread = threading.Thread(target=print, args=(f"\nGot Packet: {data}",), daemon=True)
            thread.start()
        except:
            print("\n[Connection lost]")
            break

def start_chat():
    mode = input("Enter 's' for Server or 'c' for Client: ").lower()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if mode == 's':
        sock.bind(('127.0.0.1', 5050))
        sock.listen(1)
        conn, addr = sock.accept()
        active_conn = conn # Use the connection, not the listener
    else:
        sock.connect(('127.0.0.1', 5050))
        active_conn = sock

    thread = threading.Thread(target=receive_messages, args=(active_conn,), daemon=True)
    thread.start()

    return active_conn


sock = start_chat()
