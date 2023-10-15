import threading, socket, time

def client(infos):
    ip=infos[0]
    port=infos[1]
    pseudo=infos[2]

    print("launchong")
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip,port))
    sock.send(str.encode("0§"+pseudo))
    while True:
        response=sock.recv(255)
        if response!="":
            print(response.decode("utf-8"))
        if not response:
            print("closing")
            sock.close()
            break