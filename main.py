from tkinter import Tk
from sys import argv
from graphics import Window
from startMenu import StartMenu, Game
from constants import *
from errors import errorMessage
from clientConnection import Receiver, establishConn, check_conn_status
from clientSender import Sender
import socket
import re


this_file = "main.py"

if __name__ == "__main__":
    doMainMenu = True
    online = True
    sender = None
    conn = None
    hostname = None
    port = None
    map = None

    
    for arg in argv:
        if arg == '-g':
            doMainMenu = False
        if arg == '-o':
            online = False
        if arg.startswith("-h:"):
            args = arg.split(":")
            print(args)
            if len(args) == 3:
                hostname = args[1]
                port = int(args[2])
        if arg.startswith("-m:"):
            map = arg[3:]
        
    if online:
        print("Looking for host...\n")
        if hostname == None:
            broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
            broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            broadcast_sock.settimeout(3)
            broadcast_sock.bind(("", 6100))
            try:
                data, addr = broadcast_sock.recvfrom(MAX_MESSAGE_SIZE)
                print("Received: ", data.decode('ascii'))
            except:
                print("Could not find host. Starting in single-player mode.\n")
                online = False
                broadcast_sock.close()

            if online: 
                print("Host found! Starting in two-player mode.\n")
                broadcast_sock.sendto(data, (addr))
                msg = data.decode('ascii')
                msg = msg.strip('[]')
                msg = msg.replace(",", ":")
                tokens = msg.split(":")
                broadcast_sock.close()
                if hostname == None:
                    ip_address = tokens[2]        
                
                if hostname == None:
                    hostname = tokens[1]
                    
                if port == None:
                    port = int(tokens[3])

                connResult, conn = establishConn(ip_address, port)
                if not connResult:
                    online = False
                else:
                    sender = Sender(conn)
                    print("Connected to Game Server")

    root = Tk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)
    if online:
        game = Game(root, window, sender)
    else:
        game = Game(root, window, None, map)
    mainMenu = StartMenu(root, window, game, sender, online)
    if online:
        receiver = Receiver(conn, mainMenu)
        root.protocol("WM_DELETE_WINDOW", lambda: sender.exit(root))
    
    root.after(1, lambda:check_conn_status(root))
    root.mainloop()


