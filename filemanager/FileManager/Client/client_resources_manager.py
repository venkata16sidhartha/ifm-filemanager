import os
import re
import time

class ClientResourcesManager(object):
	def __new__(cls):
		if not hasattr(cls, 'instance'):
			# craete singleton
			cls.instance = super(ClientResourcesManager, cls).__new__(cls)
		return cls.instance

	def __init__(self,resourcesDirName_ = 'resources'):
		self.resourcesDirName = resourcesDirName_		
		self.resourcesPath = os.path.join(os.getcwd(),self.resourcesDirName)
		if not os.path.isdir(self.resourcesPath):
			os.makedirs(self.resourcesPath)

	def saveFile(self,fileData,fileName,log = True):
		if self.isExistFile(fileName):
			tmpFileComponets = fileName.split('.')
			if len(tmpFileComponets) > 1:							
				newFileName = fileName[0:-(len(tmpFileComponets[-1]) + 1)]
				newFileName += '_' + str(time.time()) + '.'
				newFileName += tmpFileComponets[-1]
				fileName = newFileName
			else:
				fileName += '_' + str(time.time())

		newFile = open(os.path.join(self.resourcesPath,fileName),'wb')
		newFile.write(fileData)
		newFile.close()
		print("Saved new file: ",fileName)

	def isExistFile(self,fileName):
		filePath = os.path.join(self.resourcesPath,fileName)
		return os.path.exists(filePath)

