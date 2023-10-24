import tkinter as tk
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
        response=self.client.recv(255)
        if not response:
            a.append(False)
        else:
            a.append(True)
        a.append(response)
        self.clientReceived.put(a)
        return False


class Server():
    def __init__(self, port):
        self.port=port
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
            if not self.clientListenerStarted:
                self.clientListenerStarted=True
                self.clientListenerAnswer=queue.Queue()
                threading._start_new_thread(self.clientListener, ())
            elif not self.clientListenerAnswer.empty():
                newClient=self.clientListenerAnswer.get()
                self.clientQueues.append({"toClient":queue.Queue(),"toServer":queue.Queue()})
                threading._start_new_thread(Client, (self.clientQueues[-1],newClient))
                self.clientListenerStarted=False
            
            for k in self.clientQueues:
                if not k["toServer"].empty():
                    a=k["toServer"].get()
                    self.sendToClients(a)
                    
    def sendToClients(self, message):
        a="§".join(message)
        print(a)
        for k in self.clientQueues:
            k["toClient"].put(a)

    def clientListener(self):
        print("waiting for new client")
        client, addr=self.sock.accept()
        self.clientListenerAnswer.put((client, addr))
        return False

    def close(self):
        self.isAlive=False
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        print("server closed")
        sys.exit()

port=1234
Server(port)