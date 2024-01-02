import socket
import threading

from pygame import Surface

from chess.onlinelib import *

VERSION = "v3.2.0"
PORT = 26104


def main(win: Surface, username, password, load, ipv6=False):
    if username == "":
        showLoading(win, 8)
        return 1
    if password == "":
        showLoading(win, 9)
        return 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servaddr = ('127.0.0.1', PORT)
    try:
        sock.connect(servaddr)

    except:
        showLoading(win, 1)
        return 1

    thread = threading.Thread(target=bgThread, args=(sock,))
    thread.start()

    write(sock, username)
    write(sock, password)

    if read() != "OK":
        showLoading(win, 7)
        return 1

    write(sock, "PyChess")
    write(sock, VERSION)

    ret = 1
    msg = read()
    if msg == "errVer":
        showLoading(win, 2)

    elif msg == "errBusy":
        showLoading(win, 3)

    elif msg == "errLock":
        showLoading(win, 4)

    elif msg.startswith("key"):
        ret = lobby(win, sock, int(msg[3:]), load)
    else:
        print(msg)
        showLoading(win, 5)
    write(sock, "quit")
    sock.close()
    thread.join()
    flush()

    if ret == 2:
        showLoading(win, -1)
        return 1
    return ret
