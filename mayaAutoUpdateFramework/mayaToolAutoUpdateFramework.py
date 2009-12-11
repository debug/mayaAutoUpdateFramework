from urllib import urlopen
from xml.dom import minidom

class MayaToolAutoUpdater:
	""" checks online for updated version from XML file """
	
	# current running version of tool
	currentRunningVersion = 0.0
	feedPath = ""
	latestVersionNumber = ""
	bugFixList = ""
	newFeaturesList = ""
	newFileURL = ""
	
	def setRunningVersion(self, runningVersion):
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
		
		return self.latestVersionNumber
	
goGetUpdate = MayaToolAutoUpdater()
goGetUpdate.setRunningVersion(0.9)
goGetUpdate.setXMLPath("http://update.reality-debug.co.uk/audioAmpExtractor.xml")
goGetUpdate.getUpdateInformation()
goGetUpdate.parseFeed()