import threading
import socket
import os

localhost = '127.0.0.1'  # localhost
# publichost = os.environ['PUBLIC_IP']
port = 15207

server = socket.socket()
server.bind((localhost, port))
server.listen()

users = []
aliases = []


def send(message):
    for user in users:
        user.send(message)  # send message to all clients


def handle(user):
    while True:
        try:
            message = user.recv(1024)  # receive message from client
            mess = message.decode('ascii')
            for x in range(0, len(mess)):
                if mess[x] == ' ':
                    mess = mess[x + 1:]
                    break
            if mess == '/users':
                if len(users) == 1:
                    user.send("You are the only user on :(".encode('ascii'))
                    # user.send('You are the only user on :(')
                else:
                    for a in aliases:
                        user.send(f"{str(a)} is online.".encode('ascii'))
            elif mess[:8] == '/whisper':
                try:
                    whisper = mess[9:]  # this gives me the user + " " + message
                    recipient = ""
                    for x in range(0, len(whisper)):
                        if whisper[x] == ' ':
                            recipient = whisper[:x]  # at the next white space will tell me which part is the user
                            whisper = whisper[x + 1:]  # the rest is obviously the message
                            break
                    index = aliases.index(recipient)
                    users[index].send(f"{str(aliases[users.index(user)])} whispered to you: {whisper}".encode('ascii'))
                except:
                    user.send("Error, user does not exist most likely.".encode('ascii'))
            else:
                print(message.decode('ascii'))
                send(message)  # send to all clients
            # continuously check if a client has a message
        except:
            # if we cannot check, user has left; remove()
            remove(user)
            break


def remove(user):
    # created method for /disconnect command but command was redundant; user should just exit out of cmd
    index = users.index(user)  # find what client index is causing an error
    alias = aliases[index]  # also remove client's alias
    users.remove(user)  # remove client from array
    user.close()  # disconnect connected client
    print(f'{alias} has disconnected.')
    send(f'{alias} has left.'.encode('ascii'))  # let all users know client has left
    aliases.remove(alias)  # also pop alias from array


def connect():
    while True:
        user, ip = server.accept()  # [constantly] take users
        print(f"{str(ip)} has connected.")  # updates server

        user.send('alias'.encode('ascii'))  # send user encoded message for alias; differentiates from regular string messages
        alias = user.recv(1024).decode('ascii')  # receive alias from user
        aliases.append(alias)  # add alias
        users.append(user)  # add user to array

        print(f'{str(ip)} has joined as {alias}')  # tells the server who joined with
        send(f'{alias} has joined'.encode('ascii'))  # tells everyone who has joined
        user.send('Connection successful!'.encode('ascii'))  # confirm connection

        handling = threading.Thread(target=handle, args=(user,))
        handling.start()


print("Awaiting connections...")
connect()
