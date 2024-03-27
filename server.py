import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

IP_address = socket.gethostname()
Port = int(5000)

server.bind((IP_address, Port))

print("Accepting connections at "+IP_address+", port "+str(Port))
server.listen(5)

QUIT = "QUIT"
command = None

rows = 3
cols = 3

board = [["-"]*cols]*rows

def get_position(message):
   position = list(message)
   print(position)
   if len(position) > 2:
      print("Bad Length")
      return None, None
   if position[0].isnumeric() and position[1].isnumeric():
      row = int(position[0])
      col = int(position[1])
      if row >= 0 and row < rows and col >= 0 and col < cols:
         return row, col
   print("Bad datatype")
   return None, None

def update_board(row, col):
   if row is None or col is None:
      return False, "Invalid Coordinate"
   if board[row][col] != "x":
      board[row][col] = "x"
      return True, "Updated Successfully"
   else:
      return False, "Already Occupied"

while command != QUIT:
   conn, addr = server.accept()
   try:
      while command != QUIT:
         try:
            message = conn.recv(2048)
            if message:
               command = message.decode()
            if command != QUIT:
               row, col = get_position(command)
               valid, result = update_board(row, col)
               response = str(valid) + f" {row} {col} {result}"
               response = bytes(response, 'utf-8')
               conn.send(response)
               message = None
         except:
            continue
      if command == QUIT:
         conn.close()
   except:
      continue
print("Server Closed.")
