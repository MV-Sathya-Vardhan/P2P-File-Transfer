#SERVER PROGRAM
import os
import socket 
import threading

 

class Server:
    
    def __init__(self,location):
        self.location = location
        os.chdir(self.location)#init
        self.HEADER = 64
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.start()

 

    def handle_client(self,conn,addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MESSAGE:
                    break
                msg,feat = msg.split(',')
                if feat == "1":
                    conn.send(f"{msg},{os.path.getsize(msg)}".encode(self.FORMAT))
                elif feat == "0":
                    self.sendfile(msg,conn)
        print(f"[DISCONNECTED] {addr}")
        conn.close()

 

    def chunks(self,filename,offset,chunksize):
        tempfile_path = 'TEMP\\temp'
        with open(filename,'rb') as file:
            with open(tempfile_path,'wb') as chunk:
                file.seek(offset)
                data = file.read(chunksize)
                chunk.write(data)
        return tempfile_path

 

    def sendfile(self,msg,conn):#make temp file and copy data acc to offset
        filename, start_offset, end_offset = msg.split(';')[0], int(msg.split(';')[1]), int(msg.split(';')[2])
        temp_offset = start_offset
        chunksize = min(end_offset - start_offset , 2048000)
        data_sent = 0
        tempfile = ''
        count = 0
        while data_sent != (end_offset - start_offset):
            tempfile = self.chunks(filename,temp_offset,chunksize)
            with open(tempfile,'rb') as file:
                data = file.read()
                conn.send(data)
                data_sent += len(data)
                temp_offset += len(data)
                chunksize = min(end_offset - (data_sent + start_offset), 2048000)
            count += 1
            if count % 10 == 0:
                print("[SENDING]...")
        conn.send(b'')        
        print("[COMPLETED] Sending complete...")
    
    def start(self):
        print("[STARTING] server is starting...")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()

 

            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()