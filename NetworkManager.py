import socket
import threading
from ObjectManager import *
from TextureManager import *

enemyPlayer = create_wall((0,0,0), (1,1,0), -1)

def SendPacket(sock, data):
    try:
        sock.send(data.encode('utf-8'))
    except:
        print("Failed to send message.")

def HandlePacket(dataString: str):
    dataSplitString = dataString.split(",")
    dataInt = []

    for i in range(3):
            try:
                dataInt.append(float(dataSplitString[i]))
            except ValueError:
                print(f"Skipping invalid packet: {dataSplitString[i]} With unsplit data: {dataString}")
                return
        


    enemyPlayer.top_left = (dataInt[0], -dataInt[1], dataInt[2])
    enemyPlayer.bottom_right = (dataInt[0] + 1, -dataInt[1] + 1, dataInt[2])

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                break
            # Just printing the raw data for clarity
            thread = threading.Thread(target=HandlePacket, args=(data,), daemon=True)
            thread.start()
        except:
            print("\n[Connection lost]")
            break

        

def start_chat():
    enemyPlayer.texture = textures.GetTexture("Test")

    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('127.0.0.1', 5050))
        active_conn = sock
    except:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 5050))
        sock.listen(1)
        conn, addr = sock.accept()
        active_conn = conn # Use the connection, not the listener
        

    thread = threading.Thread(target=receive_messages, args=(active_conn,), daemon=True)
    thread.start()

    return active_conn

sock = None
