import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

h_serv = input("Please enter the host name: ")
port = 5000
server.connect((h_serv, port))

QUIT = "QUIT"

#send request to web server
print("")

cols = 3
rows = 3

board = [["-"]*cols]*rows

def update_board():
   pass

def print_board():
   for i in range(len(board)):
      print("|", end="")
      for j in range(len(board[i])):
         print(f"{board[i][j]}|", end="")
      print("\n")

print_board()

message = ""

while message != QUIT:
   message = input(f"try to send a message ({QUIT} to end)")
   request = bytes(message, 'utf-8')
   server.send(request)
   if message != QUIT:
      print("Server Response:\n")
      response = server.recv(2048)
      print(response.decode())

print("all done!")
   
   

