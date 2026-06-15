import time
import socket as sock
import customtkinter as ctk
from threading import Thread
from netifaces import interfaces, ifaddresses
from queue import Queue
from re import compile

PORT_REGEX=compile("^[0-9]{,5}$")
UPS:float=10

newMessagesQueue:Queue=Queue()

class Server:
    def __init__(self):
        self.connected:bool=False

        self.connectedUsers:list[User]=[]
        self.receivedMessagesQueue:Queue=Queue()
    
    def update(self):
        while not self.receivedMessagesQueue.empty():
            currentMsg=self.receivedMessagesQueue.get()
            if currentMsg[1]=="":
                self.connectedUsers.remove(currentMsg[0])
            else:
                print(currentMsg[1])
                newMessagesQueue.put(currentMsg[1])
        
    
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
    
    def socketListener(self):
        self.alive=True
        import sys
        while self.alive:
            data=self.socket.recv(1024)
            self.receivedMessagesQueue.put((self, data.decode("utf-8")))
            self.alive=data!=b""


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
            chatTextBox.insert("end", msg+"\n")
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