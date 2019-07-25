import socket
import sys
import os
import time

UNIX_SOCK_PIPE_PATH = "/var/run/unixsock_test.sock"  # socket file path


def serverSocket():
    # crate socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    if sock == 0:
        print('socket create error')
        return

    # bind socket
    if os.path.exists(UNIX_SOCK_PIPE_PATH):
        os.unlink(UNIX_SOCK_PIPE_PATH)
    if sock.bind(UNIX_SOCK_PIPE_PATH):
        print('socket bind error')
        return

    # listen
    if sock.listen(5):
        print("socket listen error")
        return

    print("waiting for asking question ...")
    while True:
        conn, clientAddr = sock.accept()
        try:
            data = parseRequest(conn)
            print("{0}\tReceived from client: {1}".format(time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(time.time())), bytes.decode(data)))
            time.sleep(2)  # simulate request process
            sendResponse(conn, str.encode(time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
        finally:
            conn.close()

    # close socket
    sock.close()
    # unlink socket file
    os.unlink(UNIX_SOCK_PIPE_PATH)

# parse request and get data


def parseRequest(conn):
    lenStr = conn.recv(4)
    length = int.from_bytes(lenStr, byteorder="big")  # "big"
    data = conn.recv(length)
    return data

# send response to client


def sendResponse(conn, data):
    length = len(data)
    buf = length.to_bytes(4, byteorder="big")  # "big"
    conn.sendall(buf+data)


if __name__ == "__main__":
    serverSocket()
