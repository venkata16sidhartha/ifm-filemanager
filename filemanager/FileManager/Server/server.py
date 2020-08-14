#!/bin/python
# -*- coding: utf-8 -*-
import asyncore
import socket
import os
import sys
import string
from re import match
from api import *

class MainServerSocket(asyncore.dispatcher):
  def __init__(self, port):
    asyncore.dispatcher.__init__(self)    
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'    
    try:      
      self.bind((host,port))      
      print("Socket binded")
      self.listen(1000)
    except:
      print("can't bind to socket ",host,':',port)
      sys.exit(0)     

  def handle_accept(self):
    newSocket, address = self.accept()
    print("Connected from",address)
    SecondaryServerSocket(newSocket)


class SecondaryServerSocket(asyncore.dispatcher_with_send):
  def __init__(self,socket_):
    super(SecondaryServerSocket,self).__init__(socket_)    
    self.api_manager = Api(self)

  def handle_read(self):
    receivedData = self.recv(1024**2)
    if receivedData:
      self.api_manager.receiveData(receivedData)
    else:
      self.close()

  def send_data(self, data):
    if type(data) == type(bytes("",'utf-8')):      
      self.send(data)
      self.send(bytes('','utf-8'))
    else:      
      print("Can send not binary format")

  def handle_close(self):
    print("Disconnected from: ",self.getpeername())  



if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("You must write port for socket. For example: \"$ python server.py 7000\"")
    sys.exit(1)
  else:    
    if match('^[0-9]+$',sys.argv[1]):
      MainServerSocket(int(sys.argv[1]))
      asyncore.loop()
    else:
      print("Socket port must be a number")  


