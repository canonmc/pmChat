import random
import threading
from time import sleep
from socket import *
users = []
c_sock = socket(AF_INET, SOCK_STREAM)
s_port = 12000
c_sock.connect(("localhost", s_port))
encoding = 'utf-8'
def generate_username(un):
    response = 0
    un += "#...."
    #while loop randomized integer string of length 4, response from server indicates whether or not string (username + int string) is taken
    while response < 1:
        un = un[:-4]
        for _ in range(4):
            un += str(random.randint(0,9))
        print(f"Sending {un}")
        c_sock.send(bytes(un,encoding))
        response = int(c_sock.recv(1024).decode(encoding))
        print(f"Response: {response}")
    return un

def exit():
    c_sock.close()

def send_thread():
    while 1:
        msg = input()
        if msg == "users":
            print(users)
        elif msg == "exit":
            c_sock.send(bytes(msg,encoding))
            sleep(1)
            exit()
            return
        else:
            c_sock.send(bytes((msg),encoding))

def recv_thread():
    while 1:
        msg = c_sock.recv(1024).decode(encoding)
        if msg == "exit":
            return
        if msg[0] == "\t":
            users.append(msg[1:msg.index("#")+5].strip())
        elif msg[0:2] == ".\t":
            users.remove(msg[2:msg.index("#") + 5])
        print(msg)

if __name__ == "__main__":
    username = generate_username(input("Please enter your name, or some username. Do not include numbers, as these will be randomly assigned for uniqueness\n"))
    welcome = c_sock.recv(1024).decode(encoding)
    print(welcome)
    users = welcome.split(sep = "\n")[1:-1]

    threading.Thread(target = send_thread).start()
    threading.Thread(target=recv_thread).start()
