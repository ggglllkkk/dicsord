import threading, socket, time

ip="localhost"
port=1234

print("launchong")
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip,port))

sock.send(str.encode("0§glkglkglk"))

a=True

while a:
    response=sock.recv(255)
    if response!="":
        print(response.decode('utf-8'))

print("close")
sock.close()