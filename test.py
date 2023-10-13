from threading import Thread
 
# custom thread
class CustomThread(Thread):
    # constructor
    def __init__(self):
        # execute the base constructor
        Thread.__init__(self)
        # set a default value
        self.value = None
 
    # function executed in a new thread
    def run(self):
        # store data in an instance variable
        self.value = 'Hello from a new thread'
 
# create a new thread
thread = CustomThread()
# start the thread
thread.start()
# wait for the thread to finish
thread.join()
# get the value returned from the thread
data = thread.value
print(data)