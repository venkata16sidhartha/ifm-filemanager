#!/bin/python
# -*- coding: utf-8 -*-

import pickle
import re
import base64
import xml.etree.ElementTree as ET
from resources_manager import ResourcesManager

class Api:
	def __init__(self, delegate_ = None):
		self.delegate = delegate_
		self.resources_manager = ResourcesManager()

	def receiveData(self, data):
		print(data)	
		output_data = self.queryParser(data)

		send_fun = getattr(self.delegate, 'send_data')
		if send_fun:			
			send_fun(output_data)			

	def queryParser(self, data):	
		strQuery = data.decode()
		print(strQuery)	
		if re.match('^\s*[Hh]elp\s*$',strQuery):
			return self.help()
		elif re.match('^\s*files info\s*$',strQuery):
			return self.resources_manager.getResourcesXMLData()
		#^([0-9a-zA-Z\._\- ]+,+)+[0-9a-zA-Z\._\- ]+$
		elif re.match('^([0-9a-zA-Z\._\- ]+,+)+[0-9a-zA-Z\._\- ]+$|^[0-9a-zA-Z\.\-_ ]+$',strQuery):
			return self.photosData(strQuery)
		else:
			return self.wrongQuery()

	def wrongQuery(self):
		root = ET.Element('root')
		root.attrib = {'ID':'SERVER_EXEPTION'}
		root.text = "Wrong query, try type \"Help\""
		xmlData = ET.tostring(root, encoding="utf-8")
		return xmlData	

	def help(self):
		root = ET.Element('root')
		root.attrib = {'ID':'HELP'}			
		nodeGetFilesInfo = ET.SubElement(root,'help')
		nodeGetFilesInfo.text = "To get help info send string:\"help\""

		nodeGetFilesInfo = ET.SubElement(root,'files_info')
		nodeGetFilesInfo.text = "To get files info send string:\"files info\""
		
		nodeDownloadFiles = ET.SubElement(root,'download_files')
		nodeDownloadFiles.text = "To download files send file's name or id separated by commas. Example: \"1-4,5,cat.jpg\""
		
		xmlData = ET.tostring(root, encoding="utf-8")
		return xmlData


	def photosData(self,inputString):
		newstr = re.sub(',{1,}',',',inputString)		
		#newstr = re.sub(' {1,}','',newstr)		
		fileIDs = re.split(',',newstr)
		finifhedFileIds = []
		for fileId in fileIDs:
			if re.match('^\d+\-\d+$',fileId):
				rangeIds = fileId.split('-')				
				for newId in range(int(rangeIds[0]),int(rangeIds[1]) + 1):
					finifhedFileIds.append(str(newId))
			else:
				finifhedFileIds.append(fileId)


		print(finifhedFileIds)




		dataList = self.resources_manager.getFilesDataFromList(finifhedFileIds)
		if len(dataList) == 0:
			return self.wrongQuery()

		root = ET.Element('root')
		root.attrib = {'ID':'FILES'}

		for tmpData in dataList:
			fileNode = ET.SubElement(root,'file')
			fileNode.attrib = {'name':tmpData['name']}
			b64encodedImage = base64.b64encode(tmpData['data'])
			fileNode.text = b64encodedImage.decode()
		
		xmlData = ET.tostring(root, encoding="utf-8")
		return xmlData		
