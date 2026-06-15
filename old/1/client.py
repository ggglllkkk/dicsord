import customtkinter as tk
import tkinter as ntk
import threading, socket, queue, time

isClientAlive=True

def client(infos, messageToSend, messageToIHM):
    global isClientAlive
    ip=infos[0]
    port=infos[1]
    pseudo=infos[2]
    messageToSend=messageToSend
    messageToIHM=messageToIHM
    print("launchong")
    
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print("connected to the server")
    #sock.send(messageForm("bonjour les lamis"))
    
    serverReceiveStarted=False
    serverReceived=queue.Queue()
    while isClientAlive:
        if not messageToSend.empty():
            a=messageToSend.get()
            sock.send(messageForm(a, pseudo))
            print(a)
        if not serverReceiveStarted:
            serverReceiveStarted=True
            threading._start_new_thread(serverReceiver, (sock, serverReceived))
        elif not serverReceived.empty():
            clientResponse=serverReceived.get()
            isClientAlive=clientResponse[1]
            if isClientAlive:
                messageReceived=clientResponse[0].decode("utf-8").split("§")
                #print(messageReceived)
                messageToIHM.put(clientResponse[0].decode("utf-8"))
            serverReceiveStarted=False
        time.sleep(0.001)
    print("connection ended")
    sock.close()

def serverReceiver(sock, message):
    print("waiting for new message")
    a=[]
    try: response=sock.recv(255)
    except socket.error: a.append(False)
    if a==[]: 
        a.append(True)
        a.append(response)
    message.put(a)
    return False

def messageForm(message, pseudo):
    a=[pseudo, message, str(round(time.time()))]
    b="§".join(a)
    return b.encode("utf-8")

#client(["localhost", 1234])

connected=False
connectStateList=["Connect to server", "Disconnect from server"]
sendToServ=queue.Queue()
receivedFromServ=queue.Queue()

def connectToServer():
    global thread, isClientAlive, connected
    if not connected:
        thread=threading.Thread(target=client, args=((serverAdress.get(), int(serverPort.get()), userPseudo.get()),sendToServ, receivedFromServ))
        thread.start()
        isClientAlive=True
    else:
        isClientAlive=False
    connected=not(connected)
    connectButton.configure(text=connectStateList[connected])


def sendMessage():
    sendToServ.put(messageToSend.get())

def keyPressed(key):
    if key.char=="\r" or key.char=="\n":
        sendMessage()

def writeNewLine(texte):
    messages.configure(state="normal")
    messages.insert("end", texte+"\n")
    messages.configure(state="disabled")

def beforeMain():
    if not receivedFromServ.empty():
        a=receivedFromServ.get()
        a=a.split("§")
        mTime=time.localtime(int(a[2]))
        c=f"{mTime.tm_mday}/{mTime.tm_mon} {mTime.tm_hour}:{mTime.tm_min}:{mTime.tm_sec}"
        print(a)
        b=f"<{c}>[{a[0]}] {a[1]}"
        print(b)
        writeNewLine(b)

    window.after(1, beforeMain)

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
connectButton=tk.CTkButton(optionsFrame, text=connectStateList[connected], command=connectToServer)
connectButton.grid(row=7, column=0, padx=10, pady=10)

messageLogs="exemple de texte"
messages = tk.CTkTextbox(window, state="disabled", font=MessagesFont)
messages.grid(row=0, column=0, sticky="nswe")

messageToSend=tk.StringVar()
sendMessageEntry= tk.CTkEntry(window, textvariable=messageToSend).grid(row=1, column=0, sticky="we")
sendMessageButton = tk.CTkButton(window, text="Send", command=sendMessage).grid(row=1, column=1, sticky="we")

optionsFrame.grid(row=0, column=1, sticky="nse")
beforeMain()
window.mainloop()
isClientAlive=False