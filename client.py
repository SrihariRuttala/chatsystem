from __future__ import print_function
from time import sleep
import socket,sys
import threading
import readline

CSI = '\x1b['
CLEAR = CSI + '2J'
CLEAR_LINE = CSI + '2K'
SAVE_CURSOR = CSI + 's'
UNSAVE_CURSOR = CSI + 'u'

def emit(*args):
    print(*args, sep='', end='')

def set_scroll(n):
    return CSI + '0;%dr' % n

print("client started")
s = socket.socket()
server_address = input("Enter server address : ")
server_port = 1234
try:
    print("Trying to connect to the server")
    s.connect((server_address, server_port))
    print("Connection successful")
except Exception as e:
    print("Error while connecting to the server : ")

name = input("Enter your name : ")
s.send(name.encode())

print("NOTE: TO EXIT SEND [exit] AS MESSAGE")

def recv_msg(conn):
    try:
        while True:
            server_message = conn.recv(1024).decode()
            print(server_message)
            emit(SAVE_CURSOR, GOTO_INPUT, CLEAR_LINE)
            if server_message == "[exit]":
                print("closing connection")
                s.close()
                sys.exit()
            sleep(1)
    except Exception as e:
        print("Error while receiving message")
        print(e)
        conn.close()

# Height of scrolling region
height = 40

GOTO_INPUT = CSI + '%d;0H' % (height + 1)

emit(CLEAR, set_scroll(height))

try: 
    t=threading.Thread(target=recv_msg,args=(s,))
    t.start()
    while True:
        try:
            to = input("[To] ")
            message = input("[Me] ")
        except ValueError:
            continue
        # finally:
        #     emit(UNSAVE_CURSOR)
        s.send(to.encode())
        s.send(message.encode())
        if message == "[exit]":
            print("Exitting")
            sys.exit()
except Exception as e:
    print("Error : " + str(e))
    s.close()