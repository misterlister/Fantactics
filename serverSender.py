this_file = "serverSend.py"

class ServerSender: 

    def __init__(self, serverConn):
        self.conn = serverConn

    def sendString(self,recipient, message: str):
        recipient.sendall(message.encode('ascii'))
