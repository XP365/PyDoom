import socket
import threading
from ObjectManager import *
from TextureManager import *

from collision import Vector
from numpy import atan2


PacketSize = 6

enemyPlayer = create_wall((0,0,0), (0.01,0.01,0), -1, uv_mode="stretch", double_sided=True)
enemyHit =  False


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

    def skipPacket():
        print(f"Skipping invalid packet: {dataSplitString[i]} With unsplit data: {dataString}")
    
    for i in range(PacketSize):
            try:
                dataInt.append(float(dataSplitString[i]))
            except ValueError:
                val = str(dataSplitString[i]).strip().lower()
        
                if val in ['true', 't', '1']:
                    dataInt.append(True)
                elif val in ['false', 'f', '0']:
                    dataInt.append(False)
                else:
                    print("Non-boolean string where boolean expected:", dataSplitString[i])
                    skipPacket()
                    return
                
    EnemyWidth = 1.5
    EnemyHeight = 1.5
    EnemyDepth = 1.5
    half_width = EnemyWidth / 2.0
    half_depth = EnemyDepth / 5.0
    x = dataInt[0]
    z = dataInt[2]
    enemyPlayer.top_left = (x - half_width, 0, z - half_depth)
    enemyPlayer.bottom_right = (x + half_width, -dataInt[1] + EnemyHeight, z + half_depth)
    enemyPlayer.rotation = (0, dataInt[4] - 180, 0)
    #Update hitbox position and rotation based on received data, but keep in mind the coliders are 2d on the floor
    if enemyPlayer.collider is not None:
        enemyPlayer.collider.set_points([
            Vector(enemyPlayer.top_left[0], enemyPlayer.top_left[2]),
            Vector(enemyPlayer.bottom_right[0], enemyPlayer.top_left[2]),
            Vector(enemyPlayer.bottom_right[0], enemyPlayer.bottom_right[2]),
            Vector(enemyPlayer.top_left[0], enemyPlayer.bottom_right[2])
        ])

    wasHit = dataInt[5]
    if wasHit:
        wasHit = False
        print("I was hit!")

    

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

    try:
        _sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _sock.connect(('127.0.0.1', 8081))
        active_conn = _sock
    except:
        print("Unable to find sever, hosting instead.")
        server_launcher = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Reuse address to prevent 'Address already in use' errors
        server_launcher.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_launcher.bind(('0.0.0.0', 8081))
        server_launcher.listen(1)
        
        conn, addr = server_launcher.accept()
        active_conn = conn
        
        

    thread = threading.Thread(target=receive_messages, args=(active_conn,), daemon=True)
    thread.start()

    sock = active_conn
