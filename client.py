import customtkinter as CTk
import tkinter as Tk
import threading, socket, queue, time

isClientAlive=True

def messageForm(message, pseudo=""):
    a=[pseudo, message, str(round(time.time()))]
    b="§".join(a)
    return b.encode("utf-8")

def client(infos):
    global isClientAlive
    ip=infos[0]
    port=infos[1]
    pseudo=""
    print("launchong")
    
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print("connected to the server")
    sock.send(messageForm("bonjour les lamis"))
    
    serverReceiveStarted=False
    serverReceived=queue.Queue()
    while isClientAlive:
        if not serverReceiveStarted:
            serverReceiveStarted=True
            threading._start_new_thread(serverReceiver, (sock, serverReceived))
        elif not serverReceived.empty():
            clientResponse=serverReceived.get()
            isClientAlive=clientResponse[1]
            if isClientAlive:
                messageReceived=clientResponse[0].decode("utf-8").split("§")
                print(messageReceived)
            serverReceiveStarted=False
    print("connection ended")
    sock.close()

def serverReceiver(sock, message):
    print("waiting for new message")
    a=[]
    response=sock.recv(255)
    a.append(response)
    if not response:
        a.append(False)
    else:
        a.append(True)
    message.put(a)
    return False

client(["localhost", 1234])