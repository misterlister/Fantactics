import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

IP_address = socket.gethostname()
Port = int(5000)

server.bind((IP_address, Port))

print("Accepting connections at "+IP_address+", port "+str(Port))
server.listen(5)

command = None

while True:
   conn, addr = server.accept()
   try:
      message = conn.recv(2048)
      while command != "QUIT":
         if message:
            conn.send(message) #just echo message
            command = message.decode()
            message = None
         try:
            message = conn.recv(2048)
         except:
            continue
      if command == "QUIT": 
         conn.close()
   except:
      continue

