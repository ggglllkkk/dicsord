import socket as sock
import customtkinter as ctk
from threading import Thread
from queue import Queue
from re import compile
from time import time
from datetime import datetime

"""
a="coucou les lapinsou !".encode("utf-8")

socket=sock.socket(sock.AF_INET, sock.SOCK_STREAM)
socket.connect(("127.0.0.1",8888))

import sys
b=socket.send(a)
print(sys.getsizeof(a)-33, b)

socket.close()"""

IP_REGEX=compile(r"^(((?!25?[6-9])[12]\d|[1-9])?\d\.?\b){4}$")
PORT_REGEX=compile("^[0-9]{,5}$")
UPS:float=10

newMessagesQueue=Queue()

class Client():
    def __init__(self):
        self.connected:bool=False

        self.receivedMessagesQueue:Queue=Queue()
        self.messageHistory=[]
        self.usernameDictionnary={}
        self.usernameCountDictionnary={}

    def sendMessage(self, mode:int, msg:str):
        try:
            if mode not in [0,1]: return False

            newMsg=f"{mode}{round(time())}{msg}"
            self.socket.send(newMsg.encode("utf-8"))

            return True
        except OSError as e:
            print(e, e.errno)
            return False

    def update(self):
        while not self.receivedMessagesQueue.empty():
            currentMsg=self.receivedMessagesQueue.get()
            self.messageHistory.append(currentMsg)
            newMessagesQueue.put(currentMsg)
            print(currentMsg)

            if currentMsg[0]==0:
                if not currentMsg[3] in self.usernameCountDictionnary.keys():
                    self.usernameCountDictionnary[currentMsg[3]]=0
                    self.usernameDictionnary[currentMsg[1]]=currentMsg[3]
                else:
                    self.usernameCountDictionnary[currentMsg[3]]+=1
                    self.usernameDictionnary[currentMsg[1]]=currentMsg[3]+f"({self.usernameCountDictionnary[currentMsg[3]]})"

    def toggleSocket(self):
        if self.connected==False:
            host=addressEntry.get()
            if host=="": host="127.0.0.1"
            if not IP_REGEX.match(host): return False

            port=portEntry.get()
            if not PORT_REGEX.match(port): return False
            if port=="": port=8888
            else: port=int(port)
            if port > 65365 or port <= 1024: return False

            self.socket=sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            try:
                self.socket.connect((host, port))
            except OSError as e:
                if e.errno==10061:
                    writeError("No connection could be made because the target machine actively refused it.")
                    
                    return False
                else:
                    raise e
                
            username=usernameEntry.get()
            if username=="": username="Anonymous user"
            self.sendMessage(0, username)

            self.connected=True
            print(f"Connected to server {host}:{port}")

            self.listenerThread=Thread(target=self.messageListener)
            self.listenerThread.start()

            return True
        else:
            self.socket.close()
            self.connected=False
            print("Disconnected from server")

            return True
    
    def messageListener(self):
        while self.connected:
            try:
                data=self.socket.recv(1024)
                message=data.decode("utf-8")
                message=(int(message[0]), message[1:22], int(message[22:32]), message[32:])
                self.receivedMessagesQueue.put(message)
                print("message received")
            except OSError as e:
                if e.errno == 10054:
                    self.connected=False
                    writeError("Une connexion existante a dû être fermée par l'hôte distant")
                else:
                    print(e)




def writeError(msg):
    chatTextBox.configure(state="normal")
    chatTextBox.insert("end", "[ERROR]"+msg+"\n")
    chatTextBox.tag_add("errorMessageTag", chatTextBox.index("end"+"-2l"), chatTextBox.index("end"+"-1c"))
    chatTextBox.configure(state="disabled")

def toggleClient():
    if client.toggleSocket():
        if client.connected: 
            toggleClientButton.configure(text="Stop Client")
            window.after(int(1000/UPS), update)
        else: 
            toggleClientButton.configure(text="Start Client")

def update():
    client.update()

    if not newMessagesQueue.empty():
        chatTextBox.configure(state="normal")
        while not newMessagesQueue.empty():
            msg=newMessagesQueue.get()

            if msg[0]==1:
                #chatTextBox.insert("end", f"[{msg[1]}]; {datetime.fromtimestamp(msg[2])}:\n    {msg[3]}\n")
                chatTextBox.insert("end", f"{client.usernameDictionnary[msg[1]]}: {msg[3]}\n")
                
        chatTextBox.configure(state="disabled")

    if client.connected:
        window.after(int(1000/UPS), update)

def closeWindow():
    if client.connected:
        client.toggleSocket()
    
    window.destroy()

def sendMessage():
    msg=messageTextBox.get("0.0", "end").rstrip()

    if client.connected:
        if client.sendMessage(1, msg):
            messageTextBox.delete("0.0", "end")
    else:
        writeError("Connect to server before sending message.")
        messageTextBox.delete(messageTextBox.index("end"+"-1c"), "end")

def handleEnter(event):
    if event.state&4 == 0:
        sendMessage()



client=Client()


window=ctk.CTk()
window.iconbitmap("data/dicsord.ico")
window.title("Dicsord Client")
window.geometry("800x800")
window.protocol("WM_DELETE_WINDOW", closeWindow)
window.bind("<Return>", handleEnter)

window.rowconfigure(0,weight=1)
window.columnconfigure(0,weight=1)


chatTextBox=ctk.CTkTextbox(window, state="disabled")
chatTextBox.grid(row=0, column=0, sticky="nswe")
chatTextBox.tag_config("errorMessageTag", foreground="red")

messageTextBox=ctk.CTkTextbox(window, height=50)
messageTextBox.grid(row=1,column=0, sticky="nswe")

sendMessageButton=ctk.CTkButton(window, text="Send", command=sendMessage)
sendMessageButton.grid(row=1, column=1, sticky="nswe")


settingsFrame=ctk.CTkFrame(window)
settingsFrame.grid(row=0, column=1, sticky="nswe")

addressLabel=ctk.CTkLabel(settingsFrame, text="Server address :")
addressLabel.pack()

addressEntry=ctk.CTkEntry(settingsFrame, placeholder_text="127.0.0.1")
addressEntry.pack()

portLabel=ctk.CTkLabel(settingsFrame, text="Server port :")
portLabel.pack()

portEntry=ctk.CTkEntry(settingsFrame, placeholder_text="8888")
portEntry.pack()

usernameLabel=ctk.CTkLabel(settingsFrame, text="Username :")
usernameLabel.pack()

usernameEntry=ctk.CTkEntry(settingsFrame, placeholder_text="Anonymous user")
usernameEntry.pack()

toggleClientButton=ctk.CTkButton(settingsFrame, text="Start Client", command=toggleClient)
toggleClientButton.pack(pady=10)



window.mainloop()