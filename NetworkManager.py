import socket
import threading
from ObjectManager import *
from TextureManager import *

from collision import Vector
from numpy import atan2


PacketSize = 5

enemyPlayer = create_wall((0,0,0), (0,0,0), -1, uv_mode="stretch", double_sided=True)


def SendPacket(sock, data):
    if sock == None:
        return
    try:
        sock.send(data.encode('utf-8'))
    except:
        print("Failed to send message.")

def HandlePacket(dataString: str):
    dataSplitString = dataString.split(",")
    dataInt = []

    for i in range(PacketSize):
            try:
                dataInt.append(float(dataSplitString[i]))
            except ValueError:
                print(f"Skipping invalid packet: {dataSplitString[i]} With unsplit data: {dataString}")
                return
        

    EnemyWidth = 2
    EnemyHeight = 2.3
    x = dataInt[0]
    z = dataInt[2]
    enemyPlayer.top_left = (x, 0, z)
    enemyPlayer.bottom_right = (x + EnemyWidth, -dataInt[1] + EnemyHeight, z)
    enemyPlayer.rotation = (0, -dataInt[4], 0)

    

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                break

            thread = threading.Thread(target=HandlePacket, args=(data,), daemon=True)
            thread.start()
        except:
            print("\n[Connection lost]")
            break

        
sock = None
def start_chat():
    global sock
    global enemyPlayer
    enemyPlayer.texture = textures.GetTexture("PlayerForward")

    
    _sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        _sock.connect(('172.20.136.21', 5535))
        active_conn = _sock
    except:
        _sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _sock.bind(('0.0.0.0', 5535))
        _sock.listen(1)
        conn, addr = _sock.accept()
        active_conn = conn # Use the connection, not the listener
        

    thread = threading.Thread(target=receive_messages, args=(active_conn,), daemon=True)
    thread.start()

    sock = active_conn


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable, just triggers OS to pick correct interface
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

print(get_local_ip())