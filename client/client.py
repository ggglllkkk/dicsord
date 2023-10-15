import threading, socket, time

ip="localhost"
port=1234

print("launchong")
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip,port))
time.sleep(1)
sock.send(str.encode("0§glkglkglk"))
i=True

while True:
    if i:
        sock.send(str.encode("1§bijour tt le mnd"))
        print("message sent")
        i=False
    response=sock.recv(255)
    if response!="":
        print(response.decode("utf-8"))


time.sleep(3)
print("close")
sock.close()