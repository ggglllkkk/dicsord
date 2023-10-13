import tkinter as tk
import threading, sys, socket, queue, time
from server import Server

serverAnswer=queue.Queue()
commandsToExecute=queue.Queue()
portBefore=1234

def beforeMain():
    global serverThread, portBefore
    for widgets in clientsFrame.winfo_children():
        widgets.destroy()
    if int(port.get())!=portBefore:
        print("port change detected")
        commandsToExecute.put('sys.exit()')
        serverThread=threading.Thread(target=Server, args=(int(port.get()), serverAnswer, commandsToExecute))
        serverThread.start()
    portBefore=int(port.get())
    if not serverAnswer.empty():
        a=serverAnswer.get_nowait()
        for k in a:
            tk.Label(clientsFrame, text=k).pack()
    
    window.after(10, beforeMain)

def fa():
    commandsToExecute.put('self.sendMessage("hihi; test")')

window=tk.Tk()
window.title="dicsord server"
port=tk.StringVar(value=1234)
portEntry=tk.Entry(window, textvariable=port).pack()
button=tk.Button(window, text="send to all", command=fa).pack()
clientsFrame=tk.Frame(window)
clientsFrame.pack()
beforeMain()

serverThread=threading.Thread(target=Server, args=(int(port.get()), serverAnswer, commandsToExecute))
serverThread.start()
print("IHM started")
window.mainloop()
commandsToExecute.put('sys.exit()')