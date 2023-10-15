import tkinter as tk

# [type][pseudo/IP][horodatage][contenu]

window=tk.Tk()
window.geometry("800x800")
window.title = "dicsord"
window.resizable=(0,0)
window.iconphoto(False, tk.PhotoImage(file="dicsord.png"))

dico={
    "servIp":tk.StringVar(),
    "sendMessageValue":tk.StringVar(),
    "tryToConnect":False,
    "sendMessage":False
    }

def onWindowResize(event):
    global messages
    messages.configure(wraplength=event.width)

def debug():
    print(dico)

def fconnectButton():
    dico["tryToConnect"]=True

def fsendMessageButton():
    dico["sendMessage"]=True

optionsFrame = tk.Frame(window, bg="#5A5E6B")
messageFrame = tk.Frame(window, bg="#677179")
sendMessageFrame = tk.Frame(window, bg="#16161d")
for k in range(10):
    optionsFrame.columnconfigure(k, weight=1)

ipLabel=tk.Label(optionsFrame, text="Serveur IP:").grid(row=0, column=0)
ipEntry=tk.Entry(optionsFrame, textvariable=dico["servIp"]).grid(row=0, column=1)
connectButton = tk.Button(optionsFrame, text="try connecting to serv", command=fconnectButton).grid(row=0, column=2)
debugButton = tk.Button(optionsFrame, text="debugging", command=debug).grid(row=0, column=6)


messageLogs="exemple de texte"
messages = tk.Label(messageFrame, text=messageLogs, anchor="nw",wraplength=window.winfo_width(), bg="#16161d", fg="#e9e9e2")
messages.pack(fill=tk.BOTH, expand=True)


sendMessageEntry= tk.Entry(sendMessageFrame, textvariable=dico["sendMessageValue"]).grid(row=0, column=0, sticky=tk.E)
sendMessageButton = tk.Button(sendMessageFrame, text="Envoyer", command=fsendMessageButton).grid(row=0, column=1, sticky=tk.E)

optionsFrame.pack(side=tk.TOP, fill=tk.X, expand=False)
sendMessageFrame.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
messageFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
window.bind("<Configure>", onWindowResize)
window.mainloop()