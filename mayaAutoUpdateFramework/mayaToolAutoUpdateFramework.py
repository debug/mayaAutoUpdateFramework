from urllib import urlopen
from xml.dom import minidom

class MayaToolAutoUpdater:
	""" checks online for updated version from XML file """
	
	# current running version of tool
	currentRunningVersion = 0.0
	feedPath = ""
	
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
		kulerResult = domObj.getElementsByTagName("versionNumber")
		bitref = kulerResult[0]
		print(bitref)
	
goGetUpdate = MayaToolAutoUpdater()
goGetUpdate.setRunningVersion(0.9)
goGetUpdate.setXMLPath("http://update.reality-debug.co.uk/audioAmpExtractor.xml")
goGetUpdate.getUpdateInformation()
goGetUpdate.parseFeed()