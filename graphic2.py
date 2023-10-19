import customtkinter as CTk
import tkinter as Tk

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
    dico["sendMessage"]=True
    addNewLine("chaton mignon")
    print('hmmm')

def addNewLine(texte):
    messages.configure(state="normal")
    messages.insert("end", texte+"\n")
    messages.configure(state="disabled")

def readLogs(logs):
    for widgets in messages.winfo_children():
        widgets.destroy()
    with open(logs, "r") as file:
        for k in file.readlines():
            a=k.split("§")
            if int(a)==0:
                pass
            print(k)


optionsFrame = Tk.Frame(window, bg="#5A5E6B")
messageFrame = Tk.Frame(window, bg="#677179")
sendMessageFrame = Tk.Frame(window, bg="#16161d")
#for k in range(10):
#    optionsFrame.columnconfigure(k, weight=1)
optionsFrame.columnconfigure(0, weight=1)
optionsFrame.columnconfigure(1, weight=1)
sendMessageFrame.columnconfigure(0, weight=20)
sendMessageFrame.columnconfigure(1, weight=1)

ipCTkLabel=CTk.CTkLabel(optionsFrame, text="Server IP:").grid(row=0, column=0)
ipCTkEntry=CTk.CTkEntry(optionsFrame, textvariable=dico["servIp"]).grid(row=0, column=1)
connectCTkButton = CTk.CTkButton(optionsFrame, text="Connect", command=fconnectCTkButton).grid(row=0, column=2)
#debugCTkButton = CTk.CTkButton(optionsFrame, text="debugging", command=debug).grid(row=0, column=6)


messageLogs="exemple de texte"
messages = CTk.CTkTextbox(messageFrame, state="disabled", font=MessagesFont)
messages.pack(fill=CTk.BOTH, expand=True)


sendMessageCTkEntry= CTk.CTkEntry(sendMessageFrame, textvariable=dico["sendMessageValue"]).grid(row=0, column=0, columnspan=2, sticky="nswe")
sendMessageCTkButton = CTk.CTkButton(sendMessageFrame, text="Send", command=sendMessage).grid(row=0, column=1, sticky="e")

optionsFrame.pack(side=CTk.TOP, fill=CTk.X, expand=False)
sendMessageFrame.pack(side=CTk.BOTTOM, fill=CTk.X, expand=False)
messageFrame.pack(side=CTk.BOTTOM, fill=CTk.BOTH, expand=True)
window.bind("<KeyRelease>", keyPressed)
window.mainloop()