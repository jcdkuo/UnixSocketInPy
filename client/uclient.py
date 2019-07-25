import socket
import sys
import os
import time
import threading

UNIX_SOCK_PIPE_PATH = "/var/run/unixsock_test.sock"  # socket file path


def clientSocket():
    # crate socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    if sock == 0:
        print('socket create error')
        return

    # connect server
    sock.connect(UNIX_SOCK_PIPE_PATH)

    # send message
    msg = 'tell me current time\n'
    sendRequest(sock, str.encode(msg))

    t = threading.Thread(target=onMessageReceived, args=(sock,))
    t.start()

# Send request to server, you can define your own proxy
# conn: conn handler


def sendRequest(sock, data):
    length = len(data)
    buf = length.to_bytes(4, byteorder="big")  # "big"
    sock.sendall(buf+data)


def onMessageReceived(sock):
    # while True:
    data = parseResponse(sock)
    print("{0}\tReceived from client: {1}".format(time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(time.time())), bytes.decode(data)))
    sock.close()
    #   break

# Parse request of unix socket
# conn: conn handler


def parseResponse(sock):
    lenStr = sock.recv(4)
    length = int.from_bytes(lenStr, byteorder="big")  # "big"
    data = sock.recv(length)
    return data


if __name__ == "__main__":
    clientSocket()
