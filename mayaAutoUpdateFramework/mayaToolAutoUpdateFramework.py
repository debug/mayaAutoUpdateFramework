from urllib import urlopen
from xml.dom import minidom


class MayaUpdateGUI:
	pass

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
	
	def __init__(self, currentVersion, xmlPath):
		self.setRunningVersion(currentVersion)
		self.setXMLPath(xmlPath)
	
	def setRunningVersion(self, runningVersion):
		""" sets the current running version of the script """
		self.currentRunningVersion = runningVersion
	
	def setXMLPath(self, xmlPath):
		""" set the path to the update information xml file """
		self.feedPath = xmlPath
	
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
			#print(self.latestVersionNumber)
			#in this event start maya gui showing information and offering to download
			pass
		
goGetUpdate = MayaToolAutoUpdater("0.9a", "http://update.reality-debug.co.uk/audioAmpExtractor.xml")

goGetUpdate.getUpdateInformation()
goGetUpdate.parseFeed()