import os
import sys
import urllib
from xml.dom import minidom
import maya.cmds as cmds

import locationMarker

class MayaUpdateGUI:
	
	#class variables
	
	
	def __init__(self, latestVersionNumber, productName, bugFixes, newFeatures, downloadURL):
		
		self.preferenceFileName = "mayaUpdatePrefs.prefs"
		
		self.fileDownloader = updateDownloadSystem()
		
		self.base = downloadURL[downloadURL.rindex('/')+1:]
		self.downloadURL = downloadURL
		
		self.updateInformationString = (productName + "version " + latestVersionNumber + "is now available." + "Bug fixes-" + bugFixes + "New features-" + newFeatures)
		updateInformationWindow = cmds.window(title="Software Update", iconName='Update', widthHeight=(200, 55))
		cmds.columnLayout(adjustableColumn=True)

		informationPanel = cmds.scrollField(text=self.updateInformationString, height= 400, width=300, editable=False, wordWrap=True)
		
		
		cmds.checkBox(label='Do not ask again.', onCommand=self.turnOnAutoUpdate, offCommand=self.turnOffAutoUpdate)
		
		cmds.button(label='Update', command=self.callDownloadCommand)

		cmds.button(label='Close', command=('cmds.deleteUI(\"' + updateInformationWindow + '\", window=True)'))
		cmds.setParent('..')
		cmds.showWindow(updateInformationWindow)
		
	def callDownloadCommand(self, *args):
		
		self.fileSaveDialog()
		
		self.fileDownloader.geturl(self.downloadURL, self.downloadPath)
		
	def fileSaveDialog(self, *args):

		self.downloadPath = cmds.fileDialog(mode=1, directoryMask=str(self.base))
	
	def turnOffAutoUpdate(self, *args):
		defaultPrefContents = "autoUpdateCheck = FALSE"
			
		prefFile = open((self.currentLocation() + "/" + self.preferenceFileName),"w")
		prefFile.write(defaultPrefContents)
		prefFile.close()
	
	def turnOnAutoUpdate(self, *args):
		defaultPrefContents = "autoUpdateCheck = TRUE"
			
		prefFile = open((self.currentLocation() + "/" + self.preferenceFileName),"w")
		prefFile.write(defaultPrefContents)
		prefFile.close()
	
	def currentLocation(self):
		currentDir = os.path.dirname(locationMarker.__file__)
		return currentDir
		
class updateDownloadSystem():

	def _reporthook(self, numblocks, blocksize, filesize, url=None):

		fileName = os.path.basename(url)

		try:
			percent = min((numblocks*blocksize*100)/filesize, 100)
			cmds.progressWindow(title='Download', progress=percent, status='Downloading: ', isInterruptable=True)
		except:
			percent = 100
			cmds.progressWindow(endProgress=1)

		if numblocks != 0:
			cmds.progressWindow(edit=True, progress=percent, status=('Downloading: ' + str(percent) + '%' ))
		
		
	def geturl(self, url, dst):
		
		urllib.urlretrieve(url, dst,
							lambda nb, bs, fs, url=url: self._reporthook(nb,bs,fs,url))

class MayaToolAutoUpdater:
	""" checks online for updated version from XML file """

	currentRunningVersion = ""
	feedPath = ""
	latestVersionNumber = ""
	bugFixList = ""
	newFeaturesList = ""
	newFileURL = ""
	productName = ""
	
	def __init__(self, productName, currentVersion, xmlPath):
		
		self.setRunningVersion(currentVersion)
		
		self.setProductName(productName)
		
		self.setXMLPath(xmlPath)
		
		if(self.checkPreferenceFile()):
			
			self.getUpdateInformation()
		
		else:
			pass
		
		
		
	def checkPreferenceFile(self, *args):
		preferenceFileName = "mayaUpdatePrefs.prefs"
		
		if(os.path.exists(self.currentLocation() + "/" + preferenceFileName)):
			readPrefs = open((self.currentLocation() + "/" + preferenceFileName),"r")
			updatePreference = readPrefs.read()
			readPrefs.close()
			
			if(updatePreference.count("autoUpdateCheck = TRUE")):
				updateStatus = True
			else:
				updateStatus = False

			
		else:

			defaultPrefContents = "autoUpdateCheck = TRUE"
			
			prefFile = open((self.currentLocation() + "/" + preferenceFileName),"w")
			prefFile.write(defaultPrefContents)
			prefFile.close()
			
		return updateStatus
	
	def userQueriesUpdate(self):
		if (str(self.currentRunningVersion.strip()) != str(self.latestVersionNumber.strip())):
			self.mayaGUI = MayaUpdateGUI(self.latestVersionNumber, self.productName, self.bugFixList, self.newFeaturesList, self.newFileURL)
		else:
			cmds.confirmDialog(title="wah wah wah", message="there is no update available.",button="*sighs*")

	def setRunningVersion(self, runningVersion):
		""" sets the current running version of the script """
		self.currentRunningVersion = runningVersion
	
	def setXMLPath(self, xmlPath):
		""" set the path to the update information xml file """
		self.feedPath = xmlPath
		
	def setProductName(self, productNameIn):
		self.productName = productNameIn
	
	def getUpdateInformation(self):

		try:
		
			self.updateFeed = urllib.urlopen(self.feedPath)
			
			self.parseFeed()
			
		except IOError:

			print "IO Error: Cannot to connect to 'tinternet."

	def currentLocation(self):
		currentDir = os.path.dirname(locationMarker.__file__)
		return currentDir
	
	def parseFeed(self):
		""" parses the XML feed """
		
		domObj = minidom.parseString(self.updateFeed.read())
		versionNumberResult = domObj.getElementsByTagName("versionNumber")
		bitref = versionNumberResult[0]
		self.latestVersionNumber = bitref.childNodes[0].nodeValue
		
		versionNumberResult = domObj.getElementsByTagName("bugFixes")
		bitref = versionNumberResult[0]
		self.bugFixList = bitref.childNodes[0].nodeValue
		
		versionNumberResult = domObj.getElementsByTagName("newFeatures")
		bitref = versionNumberResult[0]
		self.newFeaturesList = bitref.childNodes[0].nodeValue
		
		versionNumberResult = domObj.getElementsByTagName("fileURL")
		bitref = versionNumberResult[0]
		self.newFileURL = bitref.childNodes[0].nodeValue
		
		if (str(self.currentRunningVersion.strip()) != str(self.latestVersionNumber.strip())):
			self.mayaGUI = MayaUpdateGUI(self.latestVersionNumber, self.productName, self.bugFixList, self.newFeaturesList, self.newFileURL)
			



#goGetUpdate = MayaToolAutoUpdater("AudioAmpExtractor", "0.8a", "http://update.reality-debug.co.uk/audioAmpExtractor.xml")

#goGetUpdate.userQueriesUpdate()
