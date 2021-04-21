from socket import *
import threading
s_port = 12000
s_sock = socket(AF_INET, SOCK_STREAM)
s_sock.bind(("",s_port))
s_sock.listen(50)
encoding = 'utf-8'
#socket :: username
users = {}

def validate_un(c_sock):
    while 1:
        un = c_sock.recv(1024).decode(encoding)
        print(f"Username {un} received")
        #sends client -1 if username unavailable; client needs to recompute username
        if un in users.values():
            print(f"Username {un} not unique")
            c_sock.send(bytes("-1",encoding))
        #username accepted, notify user of acceptance
        else:
            print(f"Username {un} successfully added")
            c_sock.send(bytes("1",encoding))
            return un

def route_message(origin_user,target_user,message):
    print(f"Routing message {message} to user {target_user} from {origin_user}")
    for i in users.keys():
        if users[i] == target_user:
            i.send(bytes("<" + origin_user + ">" + " " + message,encoding))

def send_new_user_report(new_user):
    #send to all users, EXCEPT new user
    print(f"Sending new user report to users in {[i for i in users.values()]}")
    for i in users.keys():
        if i != new_user:
            i.send(bytes("\t" + users[new_user] + " just joined\n",encoding))

def send_user_list(target_user):
    print(f"Sending user list to {users[target_user]}")
    target_user.send(bytes("Welcome to the chat! Here are the users you can message:\n", encoding))
    for i in users.keys():
        if target_user != i:
            target_user.send(bytes("\t" + users[i] + "\n", encoding))

def remove_user(user_address):
    user_address.close()
    user = users[user_address]
    users.pop(user_address)
    for i in users.keys():
        i.send(bytes(".\t" + user + " just left.",encoding))

def broadcast(sender,message):
    for i in users.keys():
        if i != sender:
            i.send(bytes("From <" + users[sender] + "> to all: " + message + "\n",encoding))
# handle each client with a thread?
def handle_client(client_socket):
    un = validate_un(client_socket)
    users[client_socket] = un
    send_user_list(client_socket)
    send_new_user_report(client_socket)
    while 1:

    # message will contain target username, followed by message
        msg = client_socket.recv(1024).decode(encoding)
        if msg == "exit":
            client_socket.send(bytes("exit",encoding))
            remove_user(client_socket)
            return
        else:
            try:
                hashtag = msg.index("#")
                target = msg[:hashtag + 5]
                msg = msg[hashtag + 5:].strip()
                route_message(users[client_socket], target, msg)
            except:
                print(f"Broadcasting to all:\n\t{msg}")
                broadcast(client_socket,msg)


if __name__ == "__main__":
    print("Server started")
    while 1:
        #connection request
        c_sock, address = s_sock.accept()
        threading.Thread(target = handle_client, args = (c_sock,)).start()
