import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

h_serv = input("Please enter the host name: ")
port = 5000
server.connect((h_serv, port))

#send request to web server
print("")

message = "GET /~listerhg/index.html HTTP/1.0\r\n"
request = bytes(message, 'utf-8')
server.send(request)
print(message)

message = "\r\n"
request=bytes(message, 'utf-8')
server.send(request)

print("Server Response:\n")
response = server.recv(2048)
print(response.decode())

while message != "QUIT":
   message = input("try to send a message (QUIT to end)")
   request = bytes(message, 'utf-8')
   server.send(request)

   print("Server Response:\n")
   response = server.recv(2048)
   print(response.decode())

print("all done!")
   
   

