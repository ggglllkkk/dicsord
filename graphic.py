import tkinter as tk

# [type][pseudo/IP][horodatage][contenu]

window=tk.Tk()
window.geometry("800x800")
window.title = "dicsord"
window.resizable=(0,0)
window.iconphoto(False, tk.PhotoImage(file="data/dicsord.png"))

infoMessageFont=tk.font.Font(family="Arial", size=8, weight="bold")
userMessageFont=tk.font.Font(family="Bookman Old Style", size=12)
dico={
    "servIp":tk.StringVar(),
    "sendMessageValue":tk.StringVar(),
    "tryToConnect":False,
    "sendMessage":False
    }

def keyPressed(key):
    if key.char=="\r" or key.char=="\n":
        sendMessage()

def onWindowResize(event):
    global messages
    messages.configure(wraplength=event.width)

def debug():
    print(dico)

def fconnectButton():
    dico["tryToConnect"]=True

def sendMessage():
    dico["sendMessage"]=True

def readLogs(logs):
    for widgets in messages.winfo_children():
        widgets.destroy()
    with open(logs, "r") as file:
        for k in file.readlines():
            a=k.split("§")
            if int(a)==0:
                pass
            print(k)


optionsFrame = tk.Frame(window, bg="#5A5E6B")
messageFrame = tk.Frame(window, bg="#677179")
sendMessageFrame = tk.Frame(window, bg="#16161d")
#for k in range(10):
#    optionsFrame.columnconfigure(k, weight=1)
optionsFrame.columnconfigure(0, weight=1)
optionsFrame.columnconfigure(1, weight=1)
sendMessageFrame.columnconfigure(0, weight=20)
sendMessageFrame.columnconfigure(1, weight=1)

ipLabel=tk.Label(optionsFrame, text="Server IP:").grid(row=0, column=0)
ipEntry=tk.Entry(optionsFrame, textvariable=dico["servIp"]).grid(row=0, column=1)
connectButton = tk.Button(optionsFrame, text="Connect", command=fconnectButton).grid(row=0, column=2)
#debugButton = tk.Button(optionsFrame, text="debugging", command=debug).grid(row=0, column=6)


messageLogs="exemple de texte"
messages = tk.Frame(messageFrame, anchor="nw", bg="#16161d", fg="#e9e9e2")
messages.pack(fill=tk.BOTH, expand=True)


sendMessageEntry= tk.Entry(sendMessageFrame, textvariable=dico["sendMessageValue"]).grid(row=0, column=0, columnspan=2, sticky="nswe")
sendMessageButton = tk.Button(sendMessageFrame, text="Send", command=sendMessage).grid(row=0, column=1, sticky="e")

optionsFrame.pack(side=tk.TOP, fill=tk.X, expand=False)
sendMessageFrame.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
messageFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
window.bind("<Configure>", onWindowResize)
window.bind("<KeyRelease>", keyPressed)
window.mainloop()