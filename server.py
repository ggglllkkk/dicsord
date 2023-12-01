import customtkinter as tk
import socket, threading, time

class Client():
    def __init__(self, queues, client, isAlive):
        self.toServer=queues["toServer"]
        self.toClient=queues["toClient"]
        self.client=client
        self.isServerAlive=isAlive
        self.amAlive=[]

        self.run()
    
    def run(self):
        isWaitingForNewMessage=False
        self.newMessages=[]
        while self.isServerAlive==[] and self.amAlive==[]:
            while self.newMessages!=[]:
                a=self.newMessages.pop(0)
                if int(a.split("§")[0])==2:
                    self.amAlive.append([])
                self.toServer.append(a)
                isWaitingForNewMessage=False
            if isWaitingForNewMessage==False:
                isWaitingForNewMessage=True
                threading._start_new_thread(self.newMessageListener, ())
            while self.toClient!=[]:
                a=self.toClient.pop(0).encode("utf-8")
                try: self.client.send(a)
                except socket.error: 
                    print("an error occured during the data sending")
                    self.toClient.append(a)
        self.client.send(f"2§§§{time.time()}".encode("utf-8"))
        self.client.close()
        print("client closed")



            
    def newMessageListener(self):
        print("waiting for new message")
        try: 
            response=self.client.recv(1023).decode("utf-8")
            print(response)
            self.newMessages.append(response)
        except socket.error:
            print("connection cutted")
            self.amAlive.append([])



class Server():
    def __init__(self, port, commands, clientsList, messages, amIAlive):
        self.commands=commands
        self.clientsListToSend=clientsList
        self.messages=messages
        self.amIAlive=amIAlive
        self.newClients=[]
        self.clientQueues={}
        self.clientsList={}

        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", int(port)))
        self.sock.listen(5)

        print("server started")
        self.run()

    def run(self):
        isWaitingForNewConnection=False
        nextClientID=0
        self.isAlive=[]
        while self.isAlive==[]:
            if self.amIAlive!=[]:
                self.isAlive=False
            while self.newClients!=[]:
                a=self.newClients.pop(0)
                self.clientsList[nextClientID]={"socket":a[0], "address":a[1], "pseudo":a[1]}
                self.clientQueues[nextClientID]={"toClient":[],"toServer":[]}
                threading._start_new_thread(Client, (self.clientQueues[nextClientID],a[0],self.isAlive))
                print(f"new client: id:{nextClientID}, address:{a[1]}")
                nextClientID+=1
                isWaitingForNewConnection=False
            if isWaitingForNewConnection==False:
                print("guhr")
                isWaitingForNewConnection=True
                threading._start_new_thread(self.connectionHandler, ())
            self.clientQueuesHandler()
        self.sock.close()
        print("closing server")

    def clientQueuesHandler(self):
        for clientId, k in self.clientQueues.items():
            while k["toServer"]!=[]:
                a=k["toServer"].pop(0).split("§")
                if int(a[0])==0:
                    self.clientsList[clientId]["pseudo"]=a[1]
                    for k in self.clientList.values():
                        b=str({k["address"]:k["pseudo"]})
                    sendAll(f"0§§[{b}]§{str(round(time.time()))}")
                elif int(a[0])==1:
                    b=f"1§{self.clientsList[clientId]['address']}§{'§'.join(a[1:])}"
                    self.sendAll(b)
                    print(b)


    
    def sendAll(self, message):
        for k in self.clientQueues.values():
            k["toClient"].append(message)



    def connectionHandler(self):
        print("waiting for new connection")
        client, addr=self.sock.accept()
        self.newClients.append((client, addr))
        

def keyPressed(key):
    if key.char=="\r" or key.char=="\n":
        sendCommand()

    window.after(1, beforeMain)

def launchServer():
    global thread, serverAlive, sayToServerState
    serverAlive=not(serverAlive)
    launchServerButton.configure(text=serverStateList[serverAlive])
    if serverAlive:
        sayToServerState=[]
        thread=threading.Thread(target=Server, args=(serverPort.get(), commands, clientsList, messages, sayToServerState))
        thread.start()
    else:
        sayToServerState.append([])

def sendCommand():
    commands.append(commandToSend.get())
    commandToSend.set("")

def writeNewLine(toWrite):
    messagesTB.configure(state="normal")
    messagesTB.insert("end", str(toWrite)+"\n")
    messagesTB.configure(state="disabled")

def beforeMain():
    print(time.time())
    """while messages!=[]:
        a=messages.pop(0).split("§")
        if a[0]=="1":
            mTime=time.localtime(int(a[3]))
            b=f"{mTime.tm_mday}/{mTime.tm_mon} {mTime.tm_hour}:{mTime.tm_min}:{mTime.tm_sec}"
            c=f"<{b}>[{a[1]}] {a[2]}"
            writeNewLine(c)"""
    window.after(1, beforeMain)

serverAlive=False
serverStateList=["Launch Server", "Shutdown Server"]
clientsList=[]
messages=[]
commands=[]
sayToServerState=[]

window=tk.CTk()
window.title("Dicsord Server")
window.geometry("800x800")
window.iconbitmap("data/dicsord.ico")

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
optionsFrame = tk.CTkFrame(window)
MessagesFont=tk.CTkFont("Alef", 17)
window.bind("<KeyRelease>", keyPressed)

adress=tk.CTkLabel(optionsFrame, text="Server adress: ").grid(row=0, column=0)
serverAdress=tk.CTkLabel(optionsFrame, text=str(socket.gethostbyname(socket.gethostname()))).grid(row=1, column=0)
serverPort=tk.StringVar()
serverPort.set(1234)
serverPortLabel=tk.CTkLabel(optionsFrame, text="Server port: ").grid(row=2, column=0)
serverPortEntry=tk.CTkEntry(optionsFrame, textvariable=serverPort).grid(row=3, column=0)
launchServerButton=tk.CTkButton(optionsFrame, text=serverStateList[0], command=launchServer)
launchServerButton.grid(row=4, column=0, pady=10)

messagesTB = tk.CTkTextbox(window, state="disabled", font=MessagesFont)
messagesTB.grid(row=0, column=0, rowspan=2, sticky="nswe")
clients = tk.CTkTextbox(window, state="disabled", font=MessagesFont)
clients.grid(row=0, column=1, sticky="nse")

commandToSend=tk.StringVar()
sendCommandEntry= tk.CTkEntry(window, textvariable=commandToSend).grid(row=2, column=0, columnspan=2, sticky="we")
sendCommandButton = tk.CTkButton(window, text="Send command", command=sendCommand).grid(row=2, column=2, sticky="we")

optionsFrame.grid(row=0, column=2, sticky="nse")
beforeMain()
window.mainloop()
sayToServerState.append([])