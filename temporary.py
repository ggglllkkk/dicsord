import customtkinter as tk
import threading, sys, socket, queue, time

class Client():
    def __init__(self, dict, clientInfos):
        self.client=clientInfos[0]
        self.addr=clientInfos[1]
        self.toReceive=dict["toClient"]
        self.toSend=dict["toServer"]
        self.isAlive=True
        print("new client instance started:", self.addr)

        self.run()
    
    def run(self):
        self.clientReceiveStarted=False
        self.clientReceived=queue.Queue()
        while self.isAlive:
            if not self.clientReceiveStarted:
                self.clientReceiveStarted=True
                threading._start_new_thread(self.clientReceiver, ())
            elif not self.clientReceived.empty():
                clientResponse=self.clientReceived.get()
                self.isAlive=clientResponse[0]
                if self.isAlive:
                    messageReceived=clientResponse[1].decode("utf-8").split("§")
                    if messageReceived[0]=="": messageReceived[0]=str(self.addr)
                    #print(messageReceived)
                    self.toSend.put(messageReceived)
                self.clientReceiveStarted=False
            if not self.toReceive.empty():
                messageToSend=self.toReceive.get()
                self.client.send(messageToSend.encode("utf-8"))

        print("connection ended")
        sys.exit()

    def clientReceiver(self):
        print("waiting for new message")
        a=[]
        response=self.client.recv(255)
        if not response:
            a.append(False)
        else:
            a.append(True)
        a.append(response)
        self.clientReceived.put(a)
        return False


class Server():
    def __init__(self, port, clients, events, commands):
        self.port=port
        self.clients=clients
        self.events=events
        self.commands=commands
        self.clientQueues=[]
        self.isAlive=True

        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", self.port))
        
        print("starting server")
        self.run()
    
    def run(self):
        self.sock.listen(5)
        self.clientListenerStarted=False
        self.clientListenerAnswer=queue.Queue()
        while self.isAlive:
            if not self.commands.empty():
                print("command received")
                command=self.commands.get()
                exec(command)
            if not self.clientListenerStarted:
                self.clientListenerStarted=True
                self.clientListenerAnswer=queue.Queue()
                threading._start_new_thread(self.clientListener, ())
            elif not self.clientListenerAnswer.empty():
                newClient=self.clientListenerAnswer.get()
                self.clientQueues.append({"toClient":queue.Queue(),"toServer":queue.Queue(), "pseudo":newClient[1]})
                threading._start_new_thread(Client, (self.clientQueues[-1],newClient))
                self.clientListenerStarted=False
            
            b=[]
            for k in self.clientQueues:
                if not k["toServer"].empty():
                    a=k["toServer"].get()
                    self.sendToClients(a)
                b.append(k["pseudo"])
            #print(b)
            self.clients.put(b)
            time.sleep(0.001)
                    
    def sendToClients(self, message):
        a="§".join(message)
        print(a)
        for k in self.clientQueues:
            k["toClient"].put(a)

    def clientListener(self):
        print("waiting for new client")
        client, addr=self.sock.accept()
        self.clientListenerAnswer.put((client, addr))
        return False

    def close(self):
        self.isAlive=False
        print("server closed")
        sys.exit()

#Server(port)
serverAlive=False
serverStateList=["Launch Server", "Shutdown Server"]
clientsList=queue.Queue()
oldClientList=[]
events=queue.Queue()
commandsToServer=queue.Queue()

def launchServer():
    global serverAlive, thread
    if not serverAlive: 
        thread=threading.Thread(target=Server, args=(int(serverPort.get()), clientsList, events, commandsToServer))
        thread.start()
    else:
        commandsToServer.put("self.close()")
    serverAlive=not(serverAlive)
    launchServerButton.configure(text=serverStateList[serverAlive])

def sendCommand():
    command=commandToSend.get()
    print(command)

def keyPressed(key):
    if key.char=="\r" or key.char=="\n":
        sendCommand()

def writeNewLine(texte):
    messages.configure(state="normal")
    messages.insert("end", texte+"\n")
    messages.configure(state="disabled")

def beforeMain():
    if not clientsList.empty():
        a=clientsList.get()
        print(a)
        #for widgets in clientsFrame.winfo_children():
        #    widgets.destroy()

    window.after(1, beforeMain)

window=tk.CTk()
window.title="Dicsord Server"
window.geometry("800x800")

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
optionsFrame = tk.CTkFrame(window)
clientsFrame = tk.CTkFrame(window)
MessagesFont=tk.CTkFont("Alef", 15)
window.bind("<KeyRelease>", keyPressed)

adress=tk.CTkLabel(optionsFrame, text="Server adress: ").grid(row=0, column=0)
serverAdress=tk.CTkLabel(optionsFrame, text=str(socket.gethostbyname(socket.gethostname()))).grid(row=1, column=0)
serverPort=tk.StringVar()
serverPort.set(1234)
serverPortLabel=tk.CTkLabel(optionsFrame, text="Server port: ").grid(row=2, column=0)
serverPortEntry=tk.CTkEntry(optionsFrame, textvariable=serverPort).grid(row=3, column=0)
launchServerButton=tk.CTkButton(optionsFrame, text=serverStateList[0], command=launchServer)
launchServerButton.grid(row=4, column=0, pady=10)

messageLogs="exemple de texte"
messages = tk.CTkTextbox(window, state="disabled", font=MessagesFont)
messages.grid(row=0, column=0, rowspan=2, sticky="nswe")

commandToSend=tk.StringVar()
sendCommandEntry= tk.CTkEntry(window, textvariable=commandToSend).grid(row=2, column=0, sticky="we")
sendCommandButton = tk.CTkButton(window, text="Send command", command=sendCommand).grid(row=2, column=1, sticky="we")

optionsFrame.grid(row=0, column=1, sticky="nsew")
clientsFrame.grid(row=1, column=1, sticky="nsew")
beforeMain()
window.mainloop()
commandsToServer.put("self.close()")