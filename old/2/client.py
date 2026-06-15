import customtkinter as tk
import socket, threading, time

def client(infos, commands, messages, amIAlive):
    adress=infos[0]
    port=infos[1]
    pseudo=infos[2]

    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((adress, port))

    print("client started")

    isAlive=amIAlive
    connectionAlive=[]
    isWaitingForNewMessage=False
    newMessages=[]
    while isAlive==[] and connectionAlive==[]:
        while newMessages!=[]:
            a=newMessages.pop(0)
            messages.append(a)
            isWaitingForNewMessage=False
        if isWaitingForNewMessage==False:
            isWaitingForNewMessage=True
            threading._start_new_thread(newMessageListener, (sock, newMessages, connectionAlive))
        while commands!=[]:
            a=commands.pop(0)
            commandsHandler(sock, a)
        
        time.sleep(0.1)

def newMessageListener(sock, newMessages, connectionAlive):
        print("waiting for new message")
        try: 
            response=sock.recv(1023).decode("utf-8")
            newMessages.append(response)
            print(response)
        except socket.error:
            print("connection cutted")
            connectionAlive.append([])

def commandsHandler(sock, command):
    if command[0]=="/" and len(command)>1:
        a=command[1:].split(" ")[0]
        print("a command has been typed:", a)
        if a=="pseudos":
            a="§".join(["1",command,str(round(time.time()))])
            sock.send(a.encode("utf-8"))
    else:
        try: 
            a="§".join(["1",command,str(round(time.time()))])
            sock.send(a.encode("utf-8"))
            print(a, "has been sent")
        except: print("an error has occured while sending the message")


def keyPressed(key):
    if key.char=="\r" or key.char=="\n":
        sendMessage()

def connectToServer():
    global thread, clientAlive, sayToClientState
    clientAlive=not(clientAlive)
    connectButton.configure(text=connectStateList[clientAlive])
    if clientAlive:
        sayToClientState=[]
        thread=threading.Thread(target=client, args=((serverAdress.get(), int(serverPort.get()), userPseudo.get()), commands, messages, sayToClientState))
        thread.start()
    else:
        sayToClientState.append([])

def sendMessage():
    if messageToSend.get()!="": 
        commands.append(messageToSend.get())
        messageToSend.set("")

def writeNewLine(toWrite):
    messagesTB.configure(state="normal")
    messagesTB.insert("end", str(toWrite)+"\n")
    messagesTB.configure(state="disabled")

def beforeMain():
    while messages!=[]:
        a=messages.pop(0).split("§")
        if a[0]=="1":
            mTime=time.localtime(int(a[3]))
            b=f"{mTime.tm_mday}/{mTime.tm_mon} {mTime.tm_hour}:{mTime.tm_min}:{mTime.tm_sec}"
            c=f"<{b}>[{a[1]}] {a[2]}"
            writeNewLine(c)

    window.after(1, beforeMain)

clientAlive=False
connectStateList=["Connect to Server", "Disconnect from Server"]
messages=[]
commands=[]
sayToClientState=[]

window=tk.CTk()
window.geometry("850x800")
window.title("dicsord")
#window.iconbitmap("data/dicsord.ico")
window.resizable=(0,0)

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
optionsFrame = tk.CTkFrame(window)
MessagesFont=tk.CTkFont("Alef", 17)
window.bind("<KeyRelease>", keyPressed)

adressLabel=tk.CTkLabel(optionsFrame, text="Server adress: ").grid(row=0, column=0, padx=10)
serverAdress=tk.StringVar()
serverAdress.set("localhost")
adressEntry=tk.CTkEntry(optionsFrame, textvariable=serverAdress).grid(row=1, column=0)
portLabel=tk.CTkLabel(optionsFrame, text="Server port: ").grid(row=3, column=0, padx=10)
serverPort=tk.StringVar()
serverPort.set(1234)
portEntry=tk.CTkEntry(optionsFrame, textvariable=serverPort).grid(row=4, column=0)
pseudoLabel=tk.CTkLabel(optionsFrame, text="pseudo: ").grid(row=5, column=0, padx=10)
userPseudo=tk.StringVar()
pseudoEntry=tk.CTkEntry(optionsFrame, textvariable=userPseudo).grid(row=6, column=0)
connectButton=tk.CTkButton(optionsFrame, text=connectStateList[clientAlive], command=connectToServer)
connectButton.grid(row=7, column=0, padx=10, pady=10)

messagesTB = tk.CTkTextbox(window, state="disabled", font=MessagesFont)
messagesTB.grid(row=0, column=0, sticky="nswe")
clients = tk.CTkTextbox(window, state="disabled", font=MessagesFont)
clients.grid(row=0, column=1, sticky="nse")

messageToSend=tk.StringVar()
sendMessageEntry= tk.CTkEntry(window, textvariable=messageToSend).grid(row=1, column=0, columnspan=2, sticky="we")
sendMessageButton = tk.CTkButton(window, text="Send", command=sendMessage).grid(row=1, column=2, sticky="we")

optionsFrame.grid(row=0, column=2, sticky="nse")
beforeMain()
window.mainloop()
sayToClientState.append([])