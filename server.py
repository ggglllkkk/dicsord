import time
import socket as sock
import customtkinter as ctk
from threading import Thread
from netifaces import interfaces, ifaddresses
from queue import Queue
from re import compile
from time import time
from datetime import datetime

PORT_REGEX=compile("^[0-9]{,5}$")
UPS:float=10
ADDRESS_FORMAT="{:0=3}"
PORT_FORMAT="{:0=5}"

newMessagesQueue:Queue=Queue()

class Server:
    def __init__(self):
        self.connected:bool=False

        self.connectedUsers:list[User]=[]
        self.receivedMessagesQueue:Queue=Queue()
        self.disconnectedUsers:Queue=Queue()
        self.messageHistory=[]
        self.usernameDictionnary={}
        self.usernameCountDictionnary={}
    
    def update(self):
        while not self.receivedMessagesQueue.empty():
            currentMsg=self.receivedMessagesQueue.get()
            if currentMsg[1]=="":
                self.disconnectedUsers.put(currentMsg[0])
            else:
                newMessagesQueue.put(currentMsg)
                self.messageHistory.append(currentMsg)
                self.sendAll(currentMsg)

                if currentMsg[1][0]==0:
                    if not currentMsg[1][2] in self.usernameCountDictionnary.keys():
                        self.usernameCountDictionnary[currentMsg[1][2]]=0
                        self.usernameDictionnary[currentMsg[0].getFormattedAddress()]=currentMsg[1][2]
                    else:
                        self.usernameCountDictionnary[currentMsg[1][2]]+=1
                        self.usernameDictionnary[currentMsg[0].getFormattedAddress()]=currentMsg[1][2]+f"({self.usernameCountDictionnary[currentMsg[1][2]]})"
        
        self.removeUsers()
    
    def sendAll(self, message):
        for user in self.connectedUsers:
            try:
                newMessage=f"{message[1][0]}{message[0].getFormattedAddress()}{message[1][1]}{message[1][2]}"
                print(newMessage)
                user.sendMessage(newMessage)
            except OSError as e:
                if e.errno == 10054:
                    self.disconnectedUsers.put(user)
                else:
                    print(e)
        print("message sent")
    
    def removeUsers(self):
        while not self.disconnectedUsers.empty():
            currentUser=self.disconnectedUsers.get()
            self.connectedUsers.remove(currentUser)
    
    def toggleSocket(self):
        if self.connected==False:
            host=addressComboBox.get()

            port=portEntry.get()
            if not PORT_REGEX.match(port): return False
            if port=="": port=8888
            else: port=int(port)
            if port > 65365 or port <= 1024: return False

            self.socket:sock.socket=sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            self.socket.bind((host, port))
            self.listenerThread:Thread=Thread(target=self.socketListener)
            self.listenerThread.start()

            self.connected=True
            print(f"Server started on {host}:{port}")

            return True
        else:

            self.socket.close()
            self.connected=False
            print("Server stopped")

            return True
    
    def socketListener(self):
        self.socket.listen(5)
        try :
            while True:
                conn, addr=self.socket.accept()
                self.connectedUsers.append(User(conn, addr, self.receivedMessagesQueue))
        except OSError as e:
            if e.errno != 10038:
                raise e


class User:
    def __init__(self, socket, address, receivedMessagesQueue):
        self.socket:sock.socket=socket
        self.address=address

        print(f"New user : {self.address}")
        
        self.receivedMessagesQueue:Queue=receivedMessagesQueue

        self.listenerThread:Thread=Thread(target=self.socketListener)
        self.listenerThread.start()
    
    def getFormattedAddress(self):
        formattedAddress=self.address[0].split(".")
        formattedAddress=".".join([ADDRESS_FORMAT.format(int(k)) for k in formattedAddress])
        return formattedAddress+":"+PORT_FORMAT.format(self.address[1])
    
    def socketListener(self):
        self.alive=True
        while self.alive:
            try:
                data=self.socket.recv(1024)
                message=data.decode("utf-8")
                message=(int(message[0]), int(message[1:11]), message[11:])
                self.receivedMessagesQueue.put((self, message))
                self.alive=data!=b""
            except OSError as e:
                if e.errno == 10054:
                    self.alive=False
                else:
                    print(e)
    
    def sendMessage(self, message):
        self.socket.send(message.encode("utf-8"))


def getAllAddresses():
    addressesList=[]
    for interface in interfaces():
        if sock.AF_INET in ifaddresses(interface):
            for link in ifaddresses(interface)[sock.AF_INET]:
                addressesList.append(link["addr"])
    return ["0.0.0.0"]+addressesList

def toggleServer():
    if server.toggleSocket():
        if server.connected: 
            toggleServerButton.configure(text="Stop Server")
            window.after(int(1000/UPS), update)
        else: 
            toggleServerButton.configure(text="Start Server")

def update():
    server.update()

    if not newMessagesQueue.empty():
        chatTextBox.configure(state="normal")
        while not newMessagesQueue.empty():
            msg=newMessagesQueue.get()
            
            if msg[1][0]==1:
                chatTextBox.insert("end", f"{server.usernameDictionnary[msg[0].getFormattedAddress()]}: {msg[1][2]}\n")
        chatTextBox.configure(state="disabled")

    if server.connected:
        window.after(int(1000/UPS), update)

def closeWindow():
    if server.connected:
        server.toggleSocket()
    
    window.destroy()


server=Server()


window=ctk.CTk()
window.iconbitmap("data/dicsord.ico")
window.title("Dicsord Server")
window.geometry("800x800")
window.protocol("WM_DELETE_WINDOW", closeWindow)

window.rowconfigure(0,weight=1)
window.columnconfigure(0,weight=1)


chatTextBox=ctk.CTkTextbox(window, state="disabled")
chatTextBox.grid(row=0, column=0, sticky="nswe")

messageTextBox=ctk.CTkTextbox(window, height=50)
messageTextBox.grid(row=1,column=0, sticky="nswe")

sendMessageButton=ctk.CTkButton(window, text="Send")
sendMessageButton.grid(row=1, column=1, sticky="nswe")


settingsFrame=ctk.CTkFrame(window)
settingsFrame.grid(row=0, column=1, sticky="nswe")

addressLabel=ctk.CTkLabel(settingsFrame, text="Hosting address :")
addressLabel.pack()

addressComboBox=ctk.CTkComboBox(settingsFrame, values=getAllAddresses())
addressComboBox.pack()

portLabel=ctk.CTkLabel(settingsFrame, text="Hosting port :")
portLabel.pack()

portEntry=ctk.CTkEntry(settingsFrame, placeholder_text="8888")
portEntry.pack()

toggleServerButton=ctk.CTkButton(settingsFrame, text="Start Server", command=toggleServer)
toggleServerButton.pack(pady=10)



window.mainloop()