import sys, os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../app')))
import app.constants as constants
from PyQt4 import QtGui, QtCore


def checkSingleProgramInstance():
	import os.path
	if(os.path.isfile(constants.LOCK_FILE_PATH)):
		if (showYesNoQuestion("It seems that %s is already running,"
							  "\n as the lock file %s exists."
							  "\n"
							  "\nContinue anyway (may cause data losses)?" %(constants.SHORT_NAME,constants.LOCK_FILE_PATH),False)):
			os.remove(constants.LOCK_FILE_PATH);
			return
		else:
			sys.exit()
	with open(constants.LOCK_FILE_PATH, 'w') as f:
		pass



def showYesNoQuestion(message, default):
	msgBox = QtGui.QMessageBox()
	msgBox.setWindowTitle('Question')
	icon = QtGui.QPixmap(constants.ICONPATH)
	msgBox.setText(message)
	msgBox.setIconPixmap(icon)
	msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
	if(default):
		msgBox.setDefaultButton(QtGui.QMessageBox.Yes)
	else:
		msgBox.setDefaultButton(QtGui.QMessageBox.No)
	return msgBox.exec_()== QtGui.QMessageBox.Yes


def selectDirectory(parent, title, initialPath):
	#app = QtGui.QApplication(sys.argv)
	chooser = QtGui.QFileDialog()
	if(os.path.isdir(initialPath)):
		chooser.setDirectory(initialPath)
	chooser.setWindowTitle(title)
	chooser.setFileMode(QtGui.QFileDialog.Directory)
	if chooser.exec_():
		newpath = os.path.abspath(str(chooser.selectedFiles()[0]))
		return newpath


def limitStringRight(max, s):
	l = len(s)
	if (l > (max - 2)):
		return "… %s" %(s[(l-max+2):l])
	else:
		return s

def getSubDirectories(dir):
	dirnames = []
	if(os.path.isdir(dir)):
		for file in os.listdir(dir):
			if file.endswith(constants.TEXT_DIR_SUFFIX) and os.path.isdir(os.path.join(dir, file)):
				dirnames.append(file)
	return sorted(dirnames)

def getTextFileList(dir):
	filenames = []
	if(os.path.isdir(dir)):
		for file in os.listdir(dir):
			if file.endswith(constants.TEXT_FILE_EXTENSION) and os.path.isfile(os.path.join(dir, file)):
				filenames.append(file)
	return sorted(filenames)

def showAboutDialog():
	msgBox = QtGui.QMessageBox()
	msgBox.setWindowTitle('About %s' %constants.SHORT_NAME)
	icon = QtGui.QPixmap(constants.ICONPATH)
	message = '%s - %s - Version %s\n' \
	          '%s\n' \
	          'Website: %s\n\n' \
	          'This program is available free of charge.\n' \
	          'This program is available free of charge.\n' \
	          'All liability shall be excluded. Use at your own risk!\n'\
	          'Any commercial use is prohibited.\n\n'\
	          'Code license: MIT License. Please read the full text \n' \
	          'at http://opensource.org/licenses/mit-license.php\n\n' \
	          '%s is inspired from LingQ (http://lingq.com) and\n' \
	          'contains code from \'Learning With Texts\' (http://lwt.sf.net).\n' \
	          '%s  uses MigLayout (http://miglayout.com).\n\n' \
	          'Currently uses Python.' \
	                                                  %(constants.SHORT_NAME,
	                                                    constants.LONG_NAME,
	                                                    constants.VERSION,
	                                                    constants.COPYRIGHT,
	                                                    constants.WEBSITE,
	                                                    constants.SHORT_NAME,
	                                                    constants.SHORT_NAME)
	msgBox.setText(message)
	msgBox.setIconPixmap(icon)
	closeButton = msgBox.addButton('Close', QtGui.QMessageBox.RejectRole)
	openButton = msgBox.addButton('Open Website', QtGui.QMessageBox.RejectRole)

	closeButton.setDefault(True)
	msgBox.exec()
	if(msgBox.clickedButton()== openButton):
		import webbrowser
		webbrowser.open(constants.WEBSITE)

def showErrorMessage(msg):
	msgBox = QtGui.QMessageBox()
	msgBox.setText(msg)
	msgBox.setWindowTitle("Error")
	msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
	msgBox.setIcon(QtGui.QMessageBox.Critical)
	msgBox.exec()

def openDirectoryInFileExplorer(dir):
	import subprocess
	import sys

	if sys.platform == 'darwin':
		subprocess.call(['open', '-R', dir])
	elif sys.platform == 'linux2':
		subprocess.call(['gnome-open', '--', dir])
	elif sys.platform == 'win32':
		subprocess.call(['explorer', dir])

def showInfoMessage(msg):
	msgBox = QtGui.QMessageBox()
	msgBox.setText(msg)
	icon = QtGui.QPixmap(constants.ICONPATH)
	msgBox.setIconPixmap(icon)
	msgBox.setWindowTitle("Information")
	msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
	msgBox.exec()

def openTextFileInEditor(dir):
	import subprocess, os
	if sys.platform.startswith('darwin'):
		subprocess.call(('open', dir))
	elif os.name == 'nt':
		os.startfile(dir)
	elif os.name == 'posix':
		subprocess.call(('xdg-open', dir))

def getClipBoardText():
	from tkinter import Tk

	r = Tk()
	# read the clipboard
	c = r.clipboard_get()
	return c

def checkFileNameOK(textName):
	return textName == replaceNonFileNameCharacters(textName)

def replaceNonFileNameCharacters(s):
	import re
	if s.startswith("."):
		s = "-" + s[1:]
	return re.sub('[\\\\\\/\\:\\\"\\*\\?\\<\\>\\|]+', '-',replaceControlCharactersWithSpace(s))

def replaceControlCharactersWithSpace(s):
	import re
	return re.sub('[\\u0000-\\u001F]+',' ', s).strip()

def escapeHTML(s):
		return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")


def createNewFile(f):
	try:
		import os
		if os.path.exists(f):
			return False
		import tempfile
		tempfile.TemporaryFile(dir=os.path.dirname(os.path.realpath(f)))
		return True
	except OSError:
		return False

def leftTrim(s):
	return s.lstrip()

def writeStringIntoFile(dir, s):
	try:
		with open(dir, 'w') as f:
			f.write(s)
		return True
	except OSError:
		return False

def renameFile(file, dest):
	return True
	msg = False
	import os
	try:
		if(os.path.exists(dest)):
			os.remove(dest)
		if(not os.path.exists(file)):
			createEmptyFile(file)
		os.rename(file, dest)
		msg = True
	except BaseException as e:
		msg = False
	return msg

def createEmptyFile(dir):
	try:
		import os
		if(os.path.exists(dir)):
			return False
		open(dir, 'a').close()
		return True
	except OSError:
		return False

def readFileIntoString(filepath):
	f = open(filepath, 'r', encoding=constants.ENCODING)
	return f.read().strip()

def openURLInDefaultBrowser(urlString):
	import webbrowser
	webbrowser.open_new(urlString)