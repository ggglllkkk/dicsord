import threading, socket, time

ip="localhost"
port=1234

print("launchong")
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip,port))

sock.send(str.encode("0§glkglkglk"))

def timer(i):
    time.sleep(i)
    return False

a=True
a=timer(5)

while a:
    response=sock.recv(255)

print("close")
sock.close()