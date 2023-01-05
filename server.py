import socket
import sys
import threading
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection_list = {}
connection_list['server'] = ""
client_map = {}
name = 'w0rm32'
print("Server Started")
try:
    s.bind(('', 1234))
except Exception as e:
    print("Error : " + str(e))
    sys.exit()

def new_client(conn, address, client_name):
    try:
        print("Thread Stated " + str(client_name))
        while True:
            to = conn.recv(1024).decode('utf-8')
            msg = conn.recv(1024).decode('utf-8')
            time.sleep(1)
            if to in connection_list:
                temp = connection_list[to]
            else:
                conn.send(b'User not connected')
                continue
                
            if msg == "[exit]":
                conn.close()
                del connection_list[client_name]
                print("Client " + str(client_name) + " disconnected from chat.")
                break
            message="From : " + str(client_name) + "(" + str(address[0]) +  ")"+ "\nmessage : " + str(msg)
            print(connection_list)
            print(message)
            temp.send(message.encode())
    except Exception as e:
        del connection_list[client_name]
        print("ERROR IN THREAD" + str(e))
        conn.close()

s.listen(5)

while True:
    conn, address = s.accept()
    print("connection received from : ",address[0])
    client_name = conn.recv(1024).decode('utf-8')
    connection_list[client_name] = conn
    message = "Hello " + str(client_name)
    conn.send(message.encode())
    t = threading.Thread(target=new_client, args=(conn,address,client_name))
    t.start()
    time.sleep(2)
