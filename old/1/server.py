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
        try: response=self.client.recv(255)
        except socket.error: a.append(False)
        if a==[]: 
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
                self.writeLogs("command received: "+command)
                exec(command)
            if not self.clientListenerStarted:
                self.clientListenerStarted=True
                self.clientListenerAnswer=queue.Queue()
                threading._start_new_thread(self.clientListener, ())
            elif not self.clientListenerAnswer.empty():
                newClient=self.clientListenerAnswer.get()
                self.clientQueues.append({"toClient":queue.Queue(),"toServer":queue.Queue(), "pseudo":newClient[1]})
                threading._start_new_thread(Client, (self.clientQueues[-1],newClient))
                self.writeLogs("new client instance: "+str(newClient[1]))
                self.clientListenerStarted=False
            
            b=[]
            for k in self.clientQueues:
                if not k["toServer"].empty():
                    a=k["toServer"].get()
                    self.sendToClients(a)
                b.append(k["pseudo"])
            #print(b)
            if not self.client.full(): self.clients.put_nowait(b)
            time.sleep(0.1)
                
    def sendToClients(self, message):
        self.writeLogs(str(message))
        a="§".join(message)
        #print(a)
        for k in self.clientQueues:
            k["toClient"].put(a)
        self.events.put(a)

    def clientListener(self):
        print("waiting for new client")
        self.writeLogs("waiting for new connection")
        client, addr=self.sock.accept()
        self.clientListenerAnswer.put((client, addr))
        return False

    def close(self):
        self.isAlive=False
        print("server closed")
        self.writeLogs("server closes")
        sys.exit()

    def writeLogs(self, text):
        mTime=time.localtime(time.time())
        a=f"{mTime.tm_mday}/{mTime.tm_mon}/{mTime.tm_year} {mTime.tm_hour}:{mTime.tm_min}:{mTime.tm_sec}"
        with open("serverLogs.txt", "a") as file: file.write(a+"// "+text+"\n")

#Server(port)
serverAlive=False
serverStateList=["Launch Server", "Shutdown Server"]
clientsList=queue.Queue(1)
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
    mTime=time.localtime(time.time())
    a=f"{mTime.tm_mday}/{mTime.tm_mon}/{mTime.tm_year} {mTime.tm_hour}:{mTime.tm_min}:{mTime.tm_sec}"
    with open("serverLogs.txt", "a") as file: file.write(f"\n#### new server on port {serverPort.get()} the {a} ####\n")

def sendCommand():
    command=commandToSend.get()
    print(command)

def keyPressed(key):
    if key.char=="\r" or key.char=="\n":
        sendCommand()

def writeNewLine(texte):
    messages.configure(state="normal")
    messages.insert("end", str(texte)+"\n")
    messages.configure(state="disabled")
    with open("serverLogs.txt", "a") as file: file.write(texte+"\n")

def writeNewClient(texte):
    clients.configure(state="normal")
    clients.insert("end", str(texte)+"\n")
    clients.configure(state="disabled")

def beforeMain():
    global oldClientList
    if not clientsList.empty():
        a=clientsList.get_nowait()
        if a!=oldClientList:
            print(a)
            clients.delete("0.0")
            for k in a:
                writeNewClient(k)
            oldClientList=a
    if not events.empty():
        a=events.get_nowait()
        a=a.split("§")
        mTime=time.localtime(int(a[2]))
        c=f"{mTime.tm_mday}/{mTime.tm_mon} {mTime.tm_hour}:{mTime.tm_min}:{mTime.tm_sec}"
        print(a)
        b=f"<{c}>[{a[0]}] {a[1]}"
        writeNewLine(b)
    #print(time.time())

    window.after(1, beforeMain)

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

messages = tk.CTkTextbox(window, state="disabled", font=MessagesFont)
messages.grid(row=0, column=0, rowspan=2, sticky="nswe")
clients = tk.CTkTextbox(window, state="disabled", font=MessagesFont)
clients.grid(row=0, column=1, sticky="nse")

commandToSend=tk.StringVar()
sendCommandEntry= tk.CTkEntry(window, textvariable=commandToSend).grid(row=2, column=0, columnspan=2, sticky="we")
sendCommandButton = tk.CTkButton(window, text="Send command", command=sendCommand).grid(row=2, column=2, sticky="we")

optionsFrame.grid(row=0, column=2, sticky="nse")
beforeMain()
window.mainloop()
commandsToServer.put("self.close()")