import tkinter as tk
import threading, sys, socket, queue, time
from server import Server

serverAnswer=queue.Queue()
commandsToExecute=queue.Queue()
portBefore=1234

class Test():
    def __init__(self, a, b, c):
        self.a=a
        self.b=b
        self.c=c

        self.run()
    
    def run(self):
        while True:
            self.b.put([0])

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
    
    window.after(1, beforeMain)


window=tk.Tk()
window.title="dicsord server"
port=tk.StringVar(value=1234)
portEntry=tk.Entry(window, textvariable=port).pack()
clientsFrame=tk.Frame(window)
clientsFrame.pack()
beforeMain()

serverThread=threading.Thread(target=Server, args=(int(port.get()), serverAnswer, commandsToExecute))
serverThread.start()
print("IHM started")
window.mainloop()
commandsToExecute.put('sys.exit()')