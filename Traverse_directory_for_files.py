from __future__ import print_function
import os, optparse
from os.path import isfile

import Constants

def parseOptions():
	global gbIsStatFileAvailable, gsDirectoryToCheck, gsStringToFind
	scriptDesc = """ This script can be used to traverse directory for files or directories. This script automates the process."""
	parser = optparse.OptionParser(usage = "%prog [options]", version = "'%prog version 1.0", description = scriptDesc, epilog = "EPILOG : I hope you may find this helpful and it makes your life a bit easier")

	parser.add_option("--Recurse", dest = "gbRecurse", action = "store_true", help="This option when used, will not let this script get into sub directories")
	parser.add_option("--DirectoryToCheck", dest = "gsDirectoryToCheck", default = os.getcwd(), help="Specify the directory to be checked here. This defaults to current directory you are working on. ")
	parser.add_option("--MultiPaths", dest = "gbMultiPaths", action = "store_true", help="This option when used, will allow users to pass multiple paths to the script")
	parser.add_option("--StatStoreLocation", dest = "gsStatStoreLocation", help="Use this option if you want to store stats/results of this script to a specific location")
	parser.add_option("--StringToFind", dest = "gsStringToFind", help="Specify the string to be checked ")
	parser.add_option("--ExactSearch", dest = "gbExactSearch", action ="store_true", default =False, help="Use this option if you want string to be matched exactly, degault = False")
	parser.add_option("--Operation", dest = "gnOperation", help="Specify the type of work you intend to get done:\n 1. Make directory structure. \n 2. Search string in all the files.")
	#this should be required and int , and with this introduce all the dependencies between options

	(sOptions, sArgs) = parser.parse_args()
	globals().update(vars(sOptions))

	if gbMultiPaths:
		gsDirectoryToCheck = [gsDirectoryToCheck]
		#Next step is assuming that all options other than with the options specified are directories only, 
		#But his has a bug since we are not able to keep a tab on the arguments after which commandline option are to be taken as additional directories
		gsDirectoryToCheck.extend( [ x for x in sArgs])
	if gbExactSearch:
		gsStringToFind = " " + gsStringToFind + " "
	gbIsStatFileAvailable = True if gsStatStoreLocation else False

def parseOptions_withArgParse():
	import argparse
	aParser = argparse.ArgumentParser(usage = "%prog [options]", version = "'%prog version 1.0", description = scriptDesc, epilog = "EPILOG : I hope you may find this helpful and it makes your life a bit easier")
	aParser.add_argumnet("--Recurse", dest = "gbRecurse", action = "store_true", help="This option when used, will not let this script get into sub directories")
	aParser.add_argumnet("--DirectoryToCheck", dest = "gsDirectoryToCheck", help="Specify the directory to be checked here")
	aParser.add_argumnet("--MultiPaths", dest = "gbMultiPaths", action = "store_true", help="This option when used, will allow users to pass multiple paths to the script")

def checkInDirectory(parentDirectory, printMessage):
	""" Function to traverse in directory to check  for some file and go into files to find something"""
	for directory in os.listdir(parentDirectory):
		sFilePath = os.path.join(parentDirectory, directory)
		if isfile( sFilePath ):
			if directory.split('.')[-1] in Constants.LIST_VALID_READABLE_FILETYPES:
				with open(sFilePath, 'r') as logFileToCheck:
					firstFind = True
					for index, line in enumerate(logFileToCheck.readlines()):
						if line.find(gsStringToFind) > -1:
							if firstFind:
								printMessage( "*" * 5 + directory + "*" * 5 + Constants.S_NEWLINE)
								firstFind = False
							messageToShow = ("%d>" %(index) + line.strip() + Constants.S_NEWLINE)
							printMessage(messageToShow)
						
		elif gbRecurse:
			checkInDirectory(os.path.join(parentDirectory, directory), printMessage)

def printDirectoryTree(parentDirectory, printMessage, tabIndex = 0):
	"""Function to print directory structure(tree) of the directory passed """
	#Since this is going to be a directory put this name in [ ]
	printMessage("\t" * tabIndex + "--> " + "[" + parentDirectory.split("\\")[-1] + "]" + Constants.S_NEWLINE)
	for directory in os.listdir(parentDirectory):
		sFilePath = os.path.join(parentDirectory, directory)
		if isfile(sFilePath):
			printMessage("\t" * (tabIndex + 1) + "--> " + directory.split("\\")[-1] + Constants.S_NEWLINE)
		else :
			if gbRecurse:
				printDirectoryTree(os.path.join(parentDirectory, directory), printMessage, tabIndex + 1)
			else:
				#if script is not on recursion then create a tab gap for folder too as in the case with file
				printMessage( "\t" * (tabIndex + 1)  + "--> " + directory.split("\\")[-1] + Constants.S_NEWLINE)

def runAction():
	global gnOperation
	if gbIsStatFileAvailable:
		#erase previous contents of file (if it already exists)
		statFile = open(gsStatStoreLocation, 'w')
		statFile.close()
	statFile = open(gsStatStoreLocation, 'a') if gbIsStatFileAvailable else None
	try :
		#could have been implemented via, with statement but,  since we are not sure that we are going to use file handle or print function.
		dictAllOptions = {
			1 : printDirectoryTree
			, 2 : checkInDirectory
		}
		gnOperation = int(gnOperation)
		userOption = dictAllOptions[gnOperation] if dictAllOptions.has_key(gnOperation) else None
		
		if userOption:
			printfunc = statFile.write if gbIsStatFileAvailable else print
			printMessage = lambda message : printfunc (message)
			if gbMultiPaths:
				for directory in gsDirectoryToCheck :
					userOption(directory, printMessage)
			else:
				userOption(gsDirectoryToCheck, printMessage)
	except:
		print("Some exception occured during [%s]" %userOption.__name__)
		pass
	finally:
		if gbIsStatFileAvailable:
			statFile.close()

## Main function
if __name__ == "__main__":
	parseOptions()
	runAction()
	