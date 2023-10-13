import time, threading

class Thread():
    def __init__(self, a, b):
        self.a=a
        self.b=b

        self.run()
    
    def run(self):
        print("started")
        while True:
            print(self.a)
            if self.a:
                print(self.a)

b=[]
t1=threading.Thread(target=Thread, args=(b,0))
t1.start()
time.sleep(1)
b.append(True)
time.sleep(0.5)
del b[0]