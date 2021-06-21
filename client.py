import socket
import threading

localhost = '127.0.0.1'
randomport = 15207

while True:
    name = input("Choose a name: ")
    if name.find(' ') != -1:
        print("Error, names cannot have spaces. Use _ or alternatives.")
    else:
        break

server = socket.socket()
server.connect((localhost, randomport))


def incoming():
    while True:
        try:
            message = server.recv(1024).decode('ascii')
            if message == 'alias':
                server.send(name.encode('ascii'))
            else:
                print(message)
        except:
            print("Connection to server was lost.")  # should only occur when server is down
            server.close()
            break


def outgoing():
    while True:
        message = f'{name}: {input("")}'
        server.send(message.encode('ascii'))

receive = threading.Thread(target=incoming)
receive.start()
write = threading.Thread(target=outgoing)
write.start()
# using threading, we can constantly take inputs and outputs
