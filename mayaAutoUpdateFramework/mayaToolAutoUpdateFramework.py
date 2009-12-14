from urllib import urlopen
from xml.dom import minidom
import maya.cmds as cmds

class MayaUpdateGUI:
	
	#class variables
	
	def __init__(self, latestVersionNumber, productName, bugFixes, newFeatures, downloadURL):
		
		self.updateInformationString = ("Version: " + latestVersionNumber + "Bug fixes-" + bugFixes + "New features-" + newFeatures)
		updateInformationWindow = cmds.window(title="There is an update available", iconName='Update information', widthHeight=(200, 55))
		cmds.columnLayout(adjustableColumn=True)

		informationPanel = cmds.scrollField(text=self.updateInformationString, height= 400, width=300, editable=False, wordWrap=True)
		
		cmds.button(label='Update')
		cmds.button(label='Do not ask again')
		cmds.button(label='Close', command=('cmds.deleteUI(\"' + updateInformationWindow + '\", window=True)'))
		cmds.setParent('..')
		cmds.showWindow(updateInformationWindow)

class MayaToolAutoUpdater:
	""" checks online for updated version from XML file """
	#todos:
	# add user called update method
	
	# current running version of tool
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
		
			self.updateFeed = urlopen(self.feedPath)
	
		except IOError:

			print "IO Error: Cannot to connect to 'tinternet."
	
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
			print(str(self.latestVersionNumber).strip())
			mayaGUI = MayaUpdateGUI(self.latestVersionNumber, self.productName, self.bugFixList, self.newFeaturesList, self.newFileURL)
			#in this event start maya gui showing information and offering to download
		
goGetUpdate = MayaToolAutoUpdater("AudioAmpExtractor", "0.8a", "http://update.reality-debug.co.uk/audioAmpExtractor.xml")

goGetUpdate.getUpdateInformation()
goGetUpdate.parseFeed()