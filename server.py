import tkinter as tk
import threading, sys, socket, queue, time

class Client():
    def __init__(self, client, serverMessages):
        self.client=client[0]
        self.addr=client[1]
        self.serverMessages=serverMessages
        self.serverMessages["pseudo"]=self.addr
        self.connectionAlive=True

        print("new client", self.addr)
        self.run()
    
    def run(self):
        response=None
        threadingRecv=False
        while self.connectionAlive:
            if response:
                a=response.decode("utf-8")
                if a!="":
                    a=a.split("§")
                    a[0]=int(a[0])
                    print("message received :", a)
                    self.messageToDo(a)
                response=None
                threadingRecv=False
            if not threadingRecv:
                recvResponse=[]
                threading._start_new_thread(self.recvThread, (recvResponse,))
                threadingRecv=True
            if recvResponse:
                response=recvResponse[0]
                self.connectionAlive=recvResponse[1]

            if not self.serverMessages["toClient"].empty():
                b=self.serverMessages["toClient"].get_nowait()
                c=b[0]+"§"+b[1]+"§"+str(time.time())
                b=str.encode(c)
                self.client.send(b)
                print("sending :", b)
            #print(self.serverMessages)
    
    def recvThread(self, a):
        print("waiting for new message")
        response=self.client.recv(255)
        a.append(response)
        if not response:
            print("client disconnected")
            a.append(False)
        else: a.append(True)
        return False

    def messageToDo(self, a):
        print(a)
        time.sleep(0.1)
        if a[0]==0:
            self.serverMessages["pseudo"]=a[1]
        if a[0]==1:
            self.serverMessages["toServ"].put(a[1])




class Server():
    def __init__(self, port):
        self.port = port
        self.clientListener=None
        self.clientListenerAnswer=[]
        self.clientsMessages=[]
        self.clientTemplate={"pseudo":None, "toServ":queue.Queue(), "toClient":queue.Queue()}

        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("",self.port))
        
        print("server started")
        self.run()
    
    def run(self):
        self.sock.listen(5)
        while True:
            if not self.clientListener:
                self.clientListener=threading.Thread(target=self.fclientListener)
                self.clientListener.start()
            if self.clientListenerAnswer:
                self.clientsMessages.append(self.clientTemplate.copy())
                threading._start_new_thread(Client, (self.clientListenerAnswer[0],self.clientsMessages[-1]))
                self.clientListener=None
                self.clientListenerAnswer=[]
            for k in self.clientsMessages:
                if not k["toServ"].empty():
                    a=k["toServ"].get()
                    for n in self.clientsMessages:
                        n["toClient"].put([k["pseudo"],a])
                        #print(n["toClient"].get())
                
            #print(self.clientListener, type(self.clientListener))
            
    def fclientListener(self):
        print("waiting for new connection")
        client=self.sock.accept()
        self.clientListenerAnswer.append(client)
        return None


#port=int(input("Port ? : "))
port=1234
Server(port)