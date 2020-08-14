import sys
import os
import re
import time
import base64
from socket import *
from threading import *
import xml.etree.ElementTree as ET
from client_resources_manager import *

HOST = '127.0.0.1'
BUFFSIZE = 1024**2 # 1 Mb

class Client:	
	def __init__(self, port):		
		self.tcpSock = socket(AF_INET, SOCK_STREAM)
		self.resources_mangaer = ClientResourcesManager()
		try:
			self.tcpSock.connect((HOST, port))
			print("Connetcted to server")
		except:
			print("connection failed")
			sys.exit(0)

	def run(self):
		self.serverCallBack()
		self.userMenu()


	def serverCallBack(self):
		def loop0():
			while True:
				self.tcpSock.setblocking(0)
				timeout = 1
				total_data = []
				start_time = time.time()
								
				while True:										
					if total_data and time.time() - start_time > timeout:						
						break
					elif time.time() - start_time > timeout * 2:											
						break

					try:
						data = self.tcpSock.recv(BUFFSIZE)						
						if data:
							total_data.append(data)							
							start_time = time.time()							
						else:
							print("Connection lost")
							self.tcpSock.close()
							sys.exit(0)
					except:
						pass
				
				if total_data:					
					total_data = b''.join(total_data)
					self.parseData(total_data)
					print('\n>>>', end="")

		t = Thread(target=loop0)		
		t.daemon = True
		t.start()

	def parseData(self,data):		
		strData = data.decode()		
		try:
			root = ET.fromstring(strData)
			print(root.attrib['ID'])			
			if root.attrib['ID'] == 'HELP':
				self.parseHelpXML(root)
			elif root.attrib['ID'] == 'FILES_INFO':
				self.parseFilesInfo(root)
			elif root.attrib['ID'] == 'SERVER_EXEPTION':
				self.parseExeptionXML(root)
			elif root.attrib['ID'] == 'FILES':
				self.parseFilesDataXML(root)

		except:
			print("Exeption during executing XML file")

	def parseHelpXML(self, root):
		print('_'*115)
		for child in root:
			print('| ',child.tag.ljust(15),'| ',child.text.ljust(90),'|')
		print('-'*115)

	def parseFilesInfo(self, root):		
		print('|',end="")		
		print('{:_^7}'.format('ID'),end="")
		print('|',end="")
		print('{:_^50}'.format('file name'),end="")
		print('|',end="")
		print('{:_^30}'.format('description'),end="")
		print('|')		
		for fileNode in root:
			print('|',fileNode[0].text.ljust(5),'|',end="")
			print(fileNode[1].text.ljust(50),'|',end="")
			print(fileNode[3].text.ljust(30),'|')
		print('-'*95)

	def parseExeptionXML(self,root):
		print("SERVER EXEPTION: ",root.text)

	def parseFilesDataXML(self,root):
		print("downloaded files")
		for fileNode in root:			
			fileEncodedData = fileNode.text.encode()
			b64denodedImage = base64.b64decode(fileEncodedData)			
			self.resources_mangaer.saveFile(b64denodedImage,fileNode.attrib['name'])

	def userMenu(self):
		print('For help info just send "help". To exit just write "exit"')
		print('\n>>>', end="")
		while True:
			command = input()
			if command == 'exit':
				self.tcpSock.close()
				sys.exit(0)
			else:
				self.tcpSock.send(bytes(command,'utf-8'))

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("You must write port for socket. For example: \"$ python client.py 7000\"")
		sys.exit(1)
	else:    
		if re.match('^[0-9]+$',sys.argv[1]):
			client = Client(int(sys.argv[1]))		
			client.run()
		else:
			print("Socket port must be a number")  
		


