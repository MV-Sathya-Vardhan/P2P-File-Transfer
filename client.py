#CLIENT PROGRAM
#CHANGE IT TO CLASS... MAKE GLOBAL VARIABLES AS CLASS VARIABLES AND FUNCTIONS AS CLASS METHODS
#LEARN OOPS CONCEPT
import os
import socket

class Client():

    def __init__(self,publicIP,Offset,filename):
        self.HEADER = 64
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = publicIP
        self.ADDR = (self.SERVER, self.PORT)
        self.Offset = Offset
        self.sourcefile = filename
        self.connect()

    def connect(self):
        self.client_ack = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #HANDSHAKE TCP
        self.client_ack.connect(self.ADDR)
        self.client_dt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #DATA TRANSFER TCP
        self.client_dt.connect(self.ADDR)

    def encoding(self,msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        return message,send_length

    def handshake(self):
        msg,length = self.encoding(self.sourcefile)
        self.client_ack.send(length)
        self.client_ack.send(msg)
        file_ack = self.client_ack.recv(1024).decode(self.FORMAT)
        self.filename,self.size = file_ack.split(',')
        print(f"{self.filename} with size {self.size} Found on SERVER! ")

    def disconnect(self):
        msg,length = self.encoding(self.DISCONNECT_MESSAGE)
        self.client_dt.send(length)
        self.client_dt.send(msg)
        self.client_ack.send(length)
        self.client_ack.send(msg)

    def receiving(self,target,location):
        msg,length = self.encoding(f"{self.filename};{self.Offset},0")
        self.client_dt.send(length)
        self.client_dt.send(msg)
        print("Started receiving")
        Receiving = True
        os.chdir(location)
        size2 = self.size
        data = ""
        while True:
            with open(target,'ab') as dest:
                data = ""
                if size2 == 0:
                    break
                data = client_dt.recv(10240)
                print(len(data))
                size2 -= len(data)
                dest.write(data)
        print("Receiving complete")
        print(os.path.getsize(target))
        self.disconnect()
    