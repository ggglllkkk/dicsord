import tkinter as tk
import threading, sys, socket, queue, time

class Client():
    def __init__(self, a, answers, toSend):
        self.client=a[0]
        self.addr=a[1]
        self.toSend=toSend
        self.answersToReturn=answers
        self.isAlive=True
        self.answers=[self.isAlive]

        print("client handler started:", self.addr)
        self.run()
    
    def run(self):
        while self.isAlive:
            if self.toSend: client.send(self.toSend)
            response=self.client.recv(255)
            if not response:
                print("connection stopped")
                self.isAlive=False
                #sys.exit()
            if response != "" and self.isAlive:
                a=response.decode("utf-8").split("§")
                print(a, self.addr)
            self.answers=[self.isAlive]
            if a: self.answers.append(a)
            #print(self.answers)
            self.answersToReturn.put(self.answers)
        


class Server():
    def __init__(self, port, sendToIHM, commandsToExecute):
        self.port=port
        self.sendToIHM=sendToIHM
        self.clientAnswers={}
        self.commandsToExecute=commandsToExecute
        self.messageToSend=str.encode("")

        print("server started")
        self.run()

    def run(self):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("", self.port))
        self.sock.listen(5)
        self.listenerThread=None
    
        while True:
            d=[]
            for key,value in self.clientAnswers.items():
                if len(value)>=2:
                    d.append(value[1]+" ; "+str(key))
                else:
                    d.append(key)
            self.sendToIHM.queue.clear()
            self.sendToIHM.put(d)
            
            if not self.commandsToExecute.empty(): exec(self.commandsToExecute.get())
            if not self.listenerThread:
                a=[]
                self.listenerThread=threading.Thread(target=self.connectionsHandler, args=(self.sock, a))
                self.listenerThread.start()
            elif a:
                print("connection detected", a[0][1])
                self.clientAnswers[a[0][1]]=[queue.Queue()]
                threading._start_new_thread(Client, (a[0], self.clientAnswers[a[0][1]][0], self.messageToSend))
                self.listenerThread=None
            c=[]
            #print(self.clientAnswers)
            for addr, receive in self.clientAnswers.items():
                if not receive[0].empty(): 
                    b=receive[0].get_nowait()
                    self.processReceived(b, addr)
                    if not b[0]:
                        c.append(addr)
            if c:
                for k in c:
                    del self.clientAnswers[k]
                    
    def connectionsHandler(self, sock, clientReturn):
        print("waiting for new connection")
        client, addr=sock.accept()
        clientReturn.append([client, addr])
    
    def processReceived(self, data, clientOriginatingFrom):
        print(data)
        if len(data)>=2:
            a=data[1]
        if int(a[0])==0 and (len(self.clientAnswers[clientOriginatingFrom])<2 or self.clientAnswers[clientOriginatingFrom][1]!=a[1]):
                self.clientAnswers[clientOriginatingFrom].append(a[1])