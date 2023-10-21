import customtkinter as CTk
import tkinter as Tk
import threading, socket, queue, time

isClientAlive=True

def client(infos):
    global isClientAlive
    ip=infos[0]
    port=infos[1]

    sock=socket.socket(socket.AF_INET, sock.SOCK_STREAM)
    sock.connect((ip, port))
    
    #while isClientAlive:




"""
toClient=["localhost", 1234, "glkglkglk", queue.Queue(), queue.Queue()]
isClientAlive=True

def client(infos):
    global isClientAlive
    ip=infos[0]
    port=infos[1]
    pseudo=infos[2]
    toSend=infos[3]
    received=infos[4]
    threadingRecv=False
    response=""

    print("launchong")
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip,port))
    #sock.send(str.encode("0§"+pseudo))
    while isClientAlive:
        if not threadingRecv:
            recvResponse=[]
            threading._start_new_thread(recvListener, (recvResponse,sock))
            threadingRecv=True
        if recvResponse:
            response=recvResponse[0]
        if response:
            a=response.decode("utf-8")
            print(a, response, )
            received.put(a)
            threadingRecv=False
            if not response[1]:
                isClientAlive=False
            response=""
        if not toSend.empty():
            b=toSend.get()
            #b="1"+pseudo+"§"+b+str(time.time())
            b="1"+"§"+b+"§"+str(time.time())
            print("sending :", b)
            sock.send(b.encode("utf-8"))
        time.sleep(0.0001)
    sock.close()
    print("closing")
    return False

def recvListener(a, sock):
    print('waiting for new message')
    response=sock.recv(255)
    a.append(response)
    print(response)
    if not response:
        print("server disconnected")
        a.append(False)
    else: a.append(True)
    return False
    print("wadahel")

# [type][pseudo/IP][horodatage][contenu]

window=CTk.CTk()
window.geometry("800x800")
window.title = "dicsord"
window.resizable=(0,0)
window.iconphoto(False, Tk.PhotoImage(file="data/dicsord.png"))

#infoMessageFont=Tk.font.Font(family="Arial", size=8, weight="bold")
#userMessageFont=Tk.font.Font(family="Bookman Old Style", size=12)
MessagesFont=CTk.CTkFont("Alef", 15)

dico={
    "servIp":CTk.StringVar(),
    "sendMessageValue":CTk.StringVar(),
    "tryToConnect":False,
    "sendMessage":False
    }

def keyPressed(key):
    if key.char=="\r" or key.char=="\n":
        sendMessage()

def debug():
    print(dico)

def fconnectCTkButton():
    dico["tryToConnect"]=True

def sendMessage():
    a=sendMessageValue.get().rstrip()
    if a!="":
        toClient[3].put(a)
        print(a)

def addNewLine(texte):
    messages.configure(state="normal")
    messages.insert("end", texte+"\n")
    messages.configure(state="disabled")

def beforeMain():
    if not toClient[4].empty():
        a=toClient[4].get().split("§")
        texte=f"{a[0]}: {a[1]}"
        addNewLine(texte)

    window.after(1, beforeMain)


optionsFrame = Tk.Frame(window, bg="#5A5E6B")
messageFrame = Tk.Frame(window, bg="#677179")
sendMessageFrame = Tk.Frame(window, bg="#16161d")
for k in range(6):
    optionsFrame.columnconfigure(k, weight=1)
sendMessageFrame.columnconfigure(0, weight=20)
sendMessageFrame.columnconfigure(1, weight=1)

serverIp=CTk.StringVar()
pseudo=CTk.StringVar()
sendMessageValue=CTk.StringVar()
oldServerIp=""
oldPseudo=""

ipCTkLabel=CTk.CTkLabel(optionsFrame, text="Server IP:").grid(row=0, column=0)
ipCTkEntry=CTk.CTkEntry(optionsFrame, textvariable=serverIp).grid(row=0, column=1)
pseudoCTkLabel=CTk.CTkLabel(optionsFrame, text="Pseudo:").grid(row=0, column=2)
pseudoCTkEntry=CTk.CTkEntry(optionsFrame, textvariable=pseudo).grid(row=0, column=3)
connectCTkButton = CTk.CTkButton(optionsFrame, text="Connect", command=fconnectCTkButton).grid(row=0, column=5)
#debugCTkButton = CTk.CTkButton(optionsFrame, text="debugging", command=debug).grid(row=0, column=6)


messageLogs="exemple de texte"
messages = CTk.CTkTextbox(messageFrame, state="disabled", font=MessagesFont)
messages.pack(fill=CTk.BOTH, expand=True)


sendMessageCTkEntry= CTk.CTkEntry(sendMessageFrame, textvariable=sendMessageValue).grid(row=0, column=0, columnspan=2, sticky="nswe")
sendMessageCTkButton = CTk.CTkButton(sendMessageFrame, text="Send", command=sendMessage).grid(row=0, column=1, sticky="e")

optionsFrame.pack(side=CTk.TOP, fill=CTk.X, expand=False)
sendMessageFrame.pack(side=CTk.BOTTOM, fill=CTk.X, expand=False)
messageFrame.pack(side=CTk.BOTTOM, fill=CTk.BOTH, expand=True)
window.bind("<KeyRelease>", keyPressed)

thread=threading.Thread(target=client, args=(toClient,))
thread.start()

beforeMain()
window.mainloop()
isClientAlive=False"""