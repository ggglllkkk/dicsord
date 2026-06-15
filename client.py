import socket as sock
import customtkinter as ctk
from queue import Queue
from re import compile

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

    def sendMessage(self, msg:str):
        try:
            self.socket.send(msg.encode("utf-8"))

            return True
        except OSError as e:
            print(e, e.errno)
            return False

    def update(self):
        pass

    def toggleSocket(self):
        if self.connected==False:
            host=addressEntry.get()
            if host=="": host="127.0.0.1"
            if not IP_REGEX.match(host): return "a"

            port=portEntry.get()
            if not PORT_REGEX.match(port): return "b"
            if port=="": port=8888
            else: port=int(port)
            if port > 65365 or port <= 1024: return "c"

            self.socket=sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            try:
                self.socket.connect((host, port))
            except OSError as e:
                if e.errno==10061:
                    writeError("[ERROR]: No connection could be made because the target machine actively refused it.")
                    
                    return False
                else:
                    raise e

            self.connected=True
            print(f"Connected to server {host}:{port}")

            return True




def writeError(msg):
    chatTextBox.configure(state="normal")
    chatTextBox.insert("end", msg+"\n")
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
            chatTextBox.insert("end", msg+"\n")
        chatTextBox.configure(state="disabled")

    if client.connected:
        window.after(int(1000/UPS), update)

def closeWindow():
    if client.connected:
        client.toggleSocket()
    
    window.destroy()

def sendMessage():
    msg=messageTextBox.get("0.0", "end").rstrip()
    print([msg])


    if client.connected: 
        if client.sendMessage(msg):
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

toggleClientButton=ctk.CTkButton(settingsFrame, text="Start Client", command=toggleClient)
toggleClientButton.pack(pady=10)



window.mainloop()