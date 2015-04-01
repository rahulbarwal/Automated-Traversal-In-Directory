
import os
from os.path import isfile

gsDirectoryToCheck = r"C:\Users"

sExitCodeOne = r"Exiting with code [1]"
sExitCodeZero = r"Exiting with code [0]"
gnTotalExitCodeOne = 0
gnTotalExitCodeZero = 0

def checkInDirectory( parentDirectory):
	global gnTotalExitCodeZero, gnTotalExitCodeOne

	for directory in os.listdir(parentDirectory):
		sFilePath = os.path.join(parentDirectory, directory)
		if isfile( sFilePath ):
			#logic to open file and 
			with open(sFilePath, 'r') as logFileToCheck:
				for line in logFileToCheck.readlines():
					#do something here...
					pass
		else:	
			checkInDirectory(os.path.join(parentDirectory, directory))
	

## Main function
checkInDirectory(gsDirectoryToCheck)