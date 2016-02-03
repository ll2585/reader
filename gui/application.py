import sys, os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../app')))
import app.languageDefs as languageDefs
import app.language as language
import app.constants as constants
from app.text import Text
from gui.textFrame import TextFrame
import threading, gui.utilities as utilities
from PyQt4 import QtGui, QtCore
import gui.preferences as preferences
import sys
from app.terms import Terms
#contains StartFrame
instance = None

def run():
	t1 = threading.Thread(target=createAndShowGUI)
	t1.start()
	t1.join()


def createAndShowGUI():
	global instance
	app = QtGui.QApplication(sys.argv)
	utilities.checkSingleProgramInstance()
	instance = Application()

	setStartFrame(StartFrame())

	getStartFrame().setVisible(True)
	sys.exit(app.exec_())


def setStartFrame(startFrame):
	global instance
	instance.startFrame = startFrame

def getStartFrame():
	return instance.startFrame

def getLanguage():
	global instance
	return instance.language

def setText(text):
	global instance
	instance.text = text

def setTerms(terms):
	global instance
	instance.terms = terms

def getLangDefs():
	global instance
	return instance.langDefs

def getText():
	global instance
	return instance.text

def getTextFrame():
	global instance
	return instance.textFrame

def setTextFrame(textFrame):
	global instance
	instance.textFrame = textFrame

def getCrammerFrame():
	global instance
	return instance.crammerFrame

def setCrammerFrame(crammerFrame):
	global instance
	instance.crammerFrame = crammerFrame

def getTerms():
	global instance
	return instance.terms

def getTermFrame():
	global instance
	return instance.termFrame

def setTermFrame(termFrame):
	global instance
	instance.termFrame = termFrame

class Application:
	def __init__(self):
		self.langDefs = languageDefs.LanguageDefinitions()
		self.textFrame = None
		self.termFrame = None
		self.text = None
		self.language = None
		self.terms = None
		self.baseDir = None
		self.startFrame = None
		self.crammerFrame = None

class StartFrame(QtGui.QMainWindow):
	def __init__(self):
		super(StartFrame, self).__init__()
		self.setWindowTitle('%s - %s %s' %(constants.SHORT_NAME, constants.LONG_NAME ,constants.SHORT_VERSION))
		self.mainPanel = QtGui.QWidget()
		mainLayout = QtGui.QVBoxLayout()
		self.mainPanel.setLayout(mainLayout)

		bar1 = QtGui.QHBoxLayout()
		bar1.addWidget(QtGui.QLabel('%s Directory:' %(constants.SHORT_NAME)))
		self.buttonToChooseMainDirectory = QtGui.QPushButton('Directory', self)
		self.buttonToChooseMainDirectory.clicked.connect(self.changeDirectory)
		bar1.addWidget(self.buttonToChooseMainDirectory)
		self.buttonToOpenMainDir = QtGui.QPushButton('View...', self)
		self.buttonToOpenMainDir.clicked.connect(self.viewDirectory)
		bar1.addWidget(self.buttonToOpenMainDir)
		mainLayout.addLayout(bar1)

		bar2 = QtGui.QHBoxLayout()
		bar2.addWidget(QtGui.QLabel('Language:'))
		self.addNewLanguageButton = QtGui.QPushButton('+', self)
		self.addNewLanguageButton.clicked.connect(self.addNewLanguage)
		bar2.addWidget(self.addNewLanguageButton)
		self.comboBoxLanguages = QtGui.QComboBox(self)
		self.comboBoxLanguages.currentIndexChanged.connect(self.comboBoxLanguagesChanged)
		bar2.addWidget(self.comboBoxLanguages)
		self.editLanguageButton = QtGui.QPushButton('Edit...', self)
		self.editLanguageButton.clicked.connect(self.editLanguage)
		bar2.addWidget(self.editLanguageButton)
		mainLayout.addLayout(bar2)

		bar3 = QtGui.QHBoxLayout()
		bar3.addWidget(QtGui.QLabel('Text:'))
		self.addNewTextButton = QtGui.QPushButton('+', self)
		self.addNewTextButton.clicked.connect(self.addNewText)
		bar3.addWidget(self.addNewTextButton)
		self.comboBoxTexts = QtGui.QComboBox(self)
		self.comboBoxTexts.currentIndexChanged.connect(self.comboBoxTextChanged)
		bar3.addWidget(self.comboBoxTexts)
		self.editTextButton = QtGui.QPushButton('Edit...', self)
		self.editTextButton.clicked.connect(self.editText)
		bar3.addWidget(self.editTextButton)
		mainLayout.addLayout(bar3)

		bar4 = QtGui.QHBoxLayout()
		self.aboutButton = QtGui.QPushButton('About...', self)
		self.aboutButton.clicked.connect(self.aboutButtonClicked)
		bar4.addWidget(self.aboutButton)
		self.generalSettingsButton = QtGui.QPushButton('General Settings...', self)
		self.generalSettingsButton.clicked.connect(self.generalSettingsButtonCicked)
		bar4.addWidget(self.generalSettingsButton)
		self.refreshButton = QtGui.QPushButton('Refresh', self)
		self.refreshButton.clicked.connect(self.refreshButtonClicked)
		bar4.addWidget(self.refreshButton)
		self.readStudyButton = QtGui.QPushButton('Read/Study...', self)
		self.readStudyButton.clicked.connect(self.readStudy)
		bar4.addWidget(self.readStudyButton)
		mainLayout.addLayout(bar4)

		self.setCentralWidget(self.mainPanel)

		self.readStudyButton.setDefault(True)

		self.setFixedSize(self.width(), self.height())
		self.inSetData = False
		self.setDataAndPack()

	def changeDirectory(self):
		dir = utilities.selectDirectory(self, "Select %s data directory..." %(constants.SHORT_NAME), os.path.expanduser('~'))
		if ((dir != None) and os.path.isdir(dir)):
				preferences.putCurrMainDir(dir)
				preferences.putDBPath(dir)
				preferences.putCurrLang("[None]")
				preferences.putCurrText("[None]")
				self.setDataAndPack()


	def viewDirectory(self):
		checkAndInitBaseDirAndLanguage()
		dir = getBaseDir()
		if (dir):
			utilities.openDirectoryInFileExplorer(dir)
		else:
			utilities.showErrorMessage("Not possible.")


	def comboBoxLanguagesChanged(self):
		if self.getCbLang().currentText():
			selectedIndex = self.getCbLang().currentIndex()
			preferences.putCurrLang(self.getCbLang().itemData(selectedIndex).getText())
			self.setDataAndPack()

	def comboBoxTextChanged(self):
		if self.getCbTexts().currentText():
			selectedIndex = self.getCbTexts().currentIndex()
			preferences.putCurrText(self.getCbTexts().itemData(selectedIndex).getText())
			self.setDataAndPack()

	def addNewLanguage(self):
		checkAndInitBaseDirAndLanguage()
		if getBaseDir():
			dlg = NewLanguageDialog()
			dlg.show()
		else:
			utilities.showErrorMessage("Not possible.")

	def editLanguage(self):
		checkAndInitBaseDirAndLanguage()
		lang = getLanguage()
		if lang:
			f = LangSettingsDialog()
			f.show()
		else:
			utilities.showErrorMessage("Not possible.")

	def addNewText(self):
		checkAndInitBaseDirAndLanguage()
		lang = getLanguage()
		if lang:
			dlg = NewTextDialog(utilities.getClipBoardText().strip())
			dlg.show()
		else:
			utilities.showErrorMessage("Not possible.")

	def editText(self):
		checkAndInitBaseDirAndLanguage()
		lang = getLanguage()
		if lang:
			currText = preferences.getCurrText()
			if currText != "<Vocabulary>":
				textFile = os.path.join(lang.getTextDir(), '%s%s' %(currText, constants.TEXT_FILE_EXTENSION))
				if os.path.isfile(textFile):
					utilities.openTextFileInEditor(textFile)
					return
		utilities.showErrorMessage("Not possible.")

	def aboutButtonClicked(self):
		utilities.showAboutDialog()

	def generalSettingsButtonCicked(self):
		generalSettings = GeneralSettingsDialog()
		generalSettings.show()

	def refreshButtonClicked(self):
		self.setDataAndPack()

	def readStudy(self):
		checkAndInitBaseDirAndLanguage()
		lang = getLanguage()
		if(lang):
			currLang = lang.getLangName()
			currText = preferences.getCurrText()
			langdir = lang.getTextDir()
			termFile = os.path.join(getBaseDir(), '%s%s' %(currLang,constants.WORDS_FILE_SUFFIX))
			terms = Terms()
			setTerms(terms)
			dbPath = os.path.join(preferences.getDBPath(), constants.DB)

			#if not terms.isLoadTermsFromFileOK(termFile):
			if not terms.isLoadTermsFromDBOK(termFile, dbPath):
				utilities.showErrorMessage("Loading Words File\n"
				                           "%s"
				                           "\n"
				                           "failed.\n\nCreating empty Words File..." %(os.path.abspath(termFile)))
			'''
			if not terms.isLoadTermsFromDBOK(termFile, dbPath):
				utilities.showErrorMessage("Loading Words File\n"
				                           "%s"
				                           "\n"
				                           "failed.\n\nCreating empty Words File..." %(os.path.abspath(termFile)))
			'''
			textFile = None
			if currText=="<Vocabulary>" :
				unknownCards = terms.getUnknownCards()
				toCrammer = []
				from crammer.model.model import Card
				for c in unknownCards:
					toCrammer.append(c)
				from gui.crammerFrame import CrammerFrame
				crammerFrame = getCrammerFrame()
				if crammerFrame:
					crammerFrame.dispose()
				crammerFrame = CrammerFrame(toCrammer)
				setCrammerFrame(crammerFrame)
				self.setVisible(False)
				crammerFrame.setVisible(True)

				#import crammer.gui.gui as crammerGui
				#crammerGui.FlashCardWindow(preExistingCards=toCrammer)

				'''do this shit later
				if terms.getData().size() > 0:
					dlg = new VocabFilterSortSettingsDialog()
					dlgResult = dlg.showDialog()
					'''
				return
			else:
				textFile = os.path.join(langdir, '%s%s' %(currText, constants.TEXT_FILE_EXTENSION))
			if os.path.isfile(textFile):
				setText(Text(textFile))
				getText().matchWithTerms()
				textFrame = getTextFrame()
				if textFrame:
					textFrame.dispose()
				textFrame = TextFrame()
				setTextFrame(textFrame)
				self.setVisible(False)
				textFrame.setVisible(True)
			else:
				utilities.showErrorMessage("%s not possible (Deleted?)." %(os.path.abspath(textFile)))
		else:
			utilities.showErrorMessage("Not possible.")
		'''
		if (lang != null) {
			if (currText.equals("<Vocabulary>")) {
				if (terms.getData().size() > 0) {
					VocabFilterSortSettingsDialog dlg = new VocabFilterSortSettingsDialog();
					int dlgResult = dlg.showDialog();
					if (dlgResult == 1) {
						textFile = Utilities.CreateTempFile("Vocabulary_",
								".tmp", langdir);
						if (!terms.saveTermsToFileForReview(textFile)) {
							Utilities
									.showErrorMessage("No Vocabulary to display.\nChange your Vocabulary Filters and try again.");
							return;
						}
					} else if (dlgResult == 2) {
						textFile = Utilities.CreateTempFile("Vocabulary_",
								".htm", langdir);
						if (!terms.saveTermsToHTMLFileForReview(textFile)) {
							Utilities
									.showErrorMessage("No Vocabulary to display.\nChange your Vocabulary Filters and try again.");
							return;
						} else {
							Utilities.openURLInDefaultBrowser(textFile
									.toURI().toString());
							return;
						}
					} else if (dlgResult == 3) {
						String s = terms.getTermsForExport();
						if (s.trim().equals("")) {
							Utilities
									.showErrorMessage("No Vocabulary to export.\nChange your Vocabulary Filters and try again.");
						} else {
							File f = Utilities.saveFileDialog(frame,
									"Save Export File",
									Utilities.getDownloadsDirectoryPath());
							if (f == null) {
								Utilities
										.showInfoMessage("Action aborted. Nothing exported.");
							} else {
								if (Utilities.writeStringIntoFile(f, s)) {
									Utilities.showInfoMessage("Export to "
											+ f.getAbsolutePath()
											+ " successful.");
								} else {
									Utilities
											.showErrorMessage("Export to "
													+ f.getAbsolutePath()
													+ " NOT successful.\nPlease try again.");
								}
							}
						}
						return;
					} else {
						return;
					}
				} else {
					Utilities.showErrorMessage("Vocabulary file is empty.");
					return;
				}
			} else {
				textFile = new File(langdir, currText
						+ Constants.TEXT_FILE_EXTENSION);
			}
			if (textFile.isFile()) {
				Application.setText(new Text(textFile));
				Application.getText().matchWithTerms();
				TextFrame textFrame = Application.getTextFrame();
				if (textFrame != null) {
					textFrame.dispose();
				}
				textFrame = new TextFrame();
				Application.setTextFrame(textFrame);
				frame.setVisible(false);
				textFrame.setVisible(true);
			} else {
				Utilities.showErrorMessage(textFile.getAbsolutePath()
						+ " not possible (Deleted?).");
			}
		} else {
			Utilities.showErrorMessage("Not possible.");
		}
			'''

	def setDataAndPack(self):
		checkAndInitBaseDirAndLanguage()
		self.setDataAndPack1()
		self.setDataAndPack1()

	def setDataAndPack1(self):
		if (self.inSetData):
			pass
		self.inSetData = True
		self.readStudyButton.setEnabled(False)
		self.addNewLanguageButton.setEnabled(False)
		self.editLanguageButton.setEnabled(False)
		self.addNewTextButton.setEnabled(False)
		self.buttonToOpenMainDir.setEnabled(False)
		self.editTextButton.setEnabled(False)

		self.comboBoxLanguages.blockSignals(True)
		self.comboBoxTexts.blockSignals(True)
		oldComboBoxIndex = self.comboBoxLanguages.currentIndex()
		oldItem = self.getCbLang().itemData(oldComboBoxIndex)
		oldComboBoxTextIndex = self.comboBoxTexts.currentIndex()
		oldTextItem = self.getCbTexts().itemData(oldComboBoxTextIndex)
		self.comboBoxLanguages.clear()
		self.comboBoxTexts.clear()
		currMainDir = preferences.getCurrMainDir()
		currLang = preferences.getCurrLang()
		currText = preferences.getCurrText()
		self.getbuttonToChooseMainDirectory().setText(
				utilities.limitStringRight(
						constants.MAX_DATA_LENGTH_START_FRAME, currMainDir))
		fcurrMainDir = getBaseDir()
		noneLang = ComboBoxItem("[None]", constants.MAX_LANG_LENGTH_START_FRAME)
		noneText = ComboBoxItem("[None]", constants.MAX_TEXT_LENGTH_START_FRAME)
		if (fcurrMainDir):
			self.addNewLanguageButton.setEnabled(True)
			self.buttonToOpenMainDir.setEnabled(True)
			langs = utilities.getSubDirectories(fcurrMainDir)
			if (not langs):
				self.comboBoxLanguages.addItem(str(noneLang),noneLang)
				self.comboBoxTexts.addItem(str(noneText),noneText)
			else:
				langMod = ''
				currIndex = -1
				for lang in langs:
					langMod = lang[:len(lang)-constants.TEXT_DIR_SUFFIX_LENGTH]
					newLang = ComboBoxItem(langMod,constants.MAX_LANG_LENGTH_START_FRAME)
					self.comboBoxLanguages.addItem(str(newLang), newLang)
					if (langMod == currLang):
						currIndex = self.comboBoxLanguages.count() - 1
				if (currIndex >= 0):
					self.comboBoxLanguages.setCurrentIndex(currIndex)
					self.editLanguageButton.setEnabled(True)
					self.addNewTextButton.setEnabled(True)
				fcurrLangDir = os.path.join(fcurrMainDir,'%s%s' %(currLang, constants.TEXT_DIR_SUFFIX))
				if(os.path.isdir(fcurrLangDir)):
					texts = utilities.getTextFileList(fcurrLangDir)
					if (not texts):
						self.comboBoxTexts.addItem(str(noneText),noneText)
					else:
						textMod = ''
						currIndexT = -1
						for text in texts:
							textMod = text[:len(text)- constants.TEXT_FILE_EXTENSION_LENGTH]
							newLang = ComboBoxItem(textMod,constants.MAX_TEXT_LENGTH_START_FRAME)
							self.comboBoxTexts.addItem(str(newLang), newLang)
							if (textMod == currText):
								currIndexT = self.comboBoxTexts.count() - 1
						textMod = "<Vocabulary>"
						newText = ComboBoxItem(textMod,constants.MAX_TEXT_LENGTH_START_FRAME)
						self.comboBoxTexts.addItem(str(newText), newText)
						if (textMod == currText):
							currIndexT = self.comboBoxTexts.count() - 1
						if (currIndexT >= 0):
							self.comboBoxTexts.setCurrentIndex(currIndexT)
						self.readStudyButton.setEnabled(True);
						self.editTextButton.setEnabled((preferences.getCurrText() != "<Vocabulary>"))
				else:
					self.comboBoxTexts.addItem(str(noneText),noneText)
		else:
			self.getbuttonToChooseMainDirectory().setText("[Select…]")
			self.comboBoxLanguages.addItem(str(noneLang),noneLang)
			self.comboBoxTexts.addItem(str(noneText),noneText)
		#pack();
		if (self.readStudyButton.isEnabled()):
			self.readStudyButton.setDefault(True)
			self.readStudyButton.setFocus()
		self.inSetData = False

		self.comboBoxLanguages.blockSignals(False)
		newItem = self.getCbLang().itemData(self.comboBoxLanguages.currentIndex())
		if((not oldItem and newItem) or (oldItem.getText() != newItem.getText())):
			self.comboBoxLanguagesChanged()

		self.comboBoxTexts.blockSignals(False)
		newTextItem = self.getCbTexts().itemData(self.comboBoxTexts.currentIndex())
		if((not oldTextItem and newTextItem) or (oldTextItem.getText() != newTextItem.getText()) and True):
			self.comboBoxTextChanged()



	def getbuttonToChooseMainDirectory(self):
		return self.buttonToChooseMainDirectory

	def getCbLang(self):
		return self.comboBoxLanguages

	def getCbTexts(self):
		return self.comboBoxTexts

def setBaseDir(thisIsAPath):
	global instance
	instance.baseDir = thisIsAPath

def setLanguage(language):
	global instance
	instance.language = language

def checkAndInitBaseDirAndLanguage():
	currMainDir = preferences.getCurrMainDir()
	if(os.path.isdir(currMainDir)):
		setBaseDir(currMainDir)
		currLang = preferences.getCurrLang()
		langdir = os.path.join(currMainDir,'%s%s'%(currLang,constants.TEXT_DIR_SUFFIX))
		langFile = os.path.join(currMainDir, '%s%s'%(currLang, constants.LANG_SETTINGS_FILE_SUFFIX))
		if (os.access(langFile, os.W_OK) and os.path.isdir(langdir) and os.path.isfile(langFile)):
			setLanguage(language.Language(langFile))
		else:
			setText(None)
			setTerms(None)
			setLanguage(None)
			preferences.putCurrText("[None]")
			preferences.putCurrLang("[None]")
	else:
		setText(None)
		setTerms(None)
		setLanguage(None)
		setBaseDir(None)
		preferences.putCurrText("[None]")
		preferences.putCurrLang("[None]")
		preferences.putCurrMainDir("[Select…]")
		preferences.putDBPath("[Select…]")

def getBaseDir():
	global instance
	return instance.baseDir

class ComboBoxItem():
	def __init__(self, text, maxLen):
		self.text = text
		self.abbrevText = '%s...' %(text[:maxLen - 1]) if (len(text) > (maxLen - 1)) else text

	def getText(self):
		return self.text

	def __str__(self):
		return self.abbrevText

class GeneralSettingsDialog(QtGui.QDialog):
	def __init__(self):
		super(GeneralSettingsDialog, self).__init__()
		self.setWindowTitle('General Settings')

		self.settingsTableModel = GeneralSettingsTableModel()
		table_view = QtGui.QTableView()
		table_view.setModel(self.settingsTableModel)
		font = QtGui.QFont("Courier New", 14)
		table_view.setFont(font)
		table_view.resizeColumnsToContents()

		self.mainLayout = QtGui.QVBoxLayout(self)
		self.mainLayout.addWidget(table_view)
		self.setLayout(self.mainLayout)
		self.exec()

class GeneralSettingsTableModel(QtCore.QAbstractTableModel):
	def __init__(self):
		super(GeneralSettingsTableModel, self).__init__()
		self.header = ['Setting', 'Value (Double Click to Edit)']
		self.mylist = []
		self.refreshMyList()

	def rowCount(self, parent):
		return len(self.mylist)

	def columnCount(self, parent):
		return len(self.mylist[0])

	def headerData(self, col, orientation, role):
		if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
			return self.header[col]
		return None

	def refreshMyList(self):
		self.mylist = [['WidthTextPanel', preferences.getCurrWidthTextPanel()],
		               ['HeightTextPanel', preferences.getCurrHeightTextPanel()],
		               ['PopupMenusNested', 1 if preferences.getCurrPopupMenusNested() else 0],
		               ['DialogFontSize%', preferences.getCurrDialogFontSizePercent()],
		               ['LookAndFeel', preferences.getCurrLookAndFeel()]]

	def data(self, index, role):
		self.refreshMyList()
		if not index.isValid():
			return None
		elif role == QtCore.Qt.EditRole:
			return self.mylist[index.row()][index.column()]  # node.data method defined above (string)
		elif role != QtCore.Qt.DisplayRole:
			return None
		return self.mylist[index.row()][index.column()]
	
	def setData(self, index, value, role=QtCore.Qt.DisplayRole):
		if index.column() != 1:
			return False
		row = index.row()
		try:
			v = int(value)
		except Exception:
			tempVals = [600, 400, 0, 100, 0]
			v = tempVals[row]
		if row == 0 :
			v = max(v, 100)
			preferences.putCurrWidthTextPanel(v)
		elif(row == 1):
			v = max(v, 100)
			preferences.putCurrHeightTextPanel(v)
		elif(row == 2):
			preferences.putCurrPopupMenusNested(v != 0)
		elif(row == 3):
			if(v < 75 or v > 150):
				utilities.showInfoMessage("Wrong Value.\nAllowed Range: 75 ... 150 %.\nSet to default: 100 %.")
				v = 100
			if(preferences.getCurrLookAndFeel() == "nimbus" and (v != 100)):
				utilities.showInfoMessage("Wrong Value.\nWith 'nimbus' Look & Feel, value must be 100 %.")
				v = 100
			preferences.putCurrDialogFontSizePercent(v)
			utilities.showInfoMessage("Dialog Font Size Change will take effect after Restart of the Program.")
		elif(row == 4):
			s = str(value)
			tempArr = ['system', 'nimbus', 'metal']
			if (s in tempArr):
				preferences.putCurrLookAndFeel(s)
				if (s == "nimbus"):
					preferences.putCurrDialogFontSizePercent(100)
			else:
				utilities.showInfoMessage("Value wrong.\nAllowed Values: 'system' / 'nimbus' / 'metal'.\nSet to default: 'system'.")
				preferences.putCurrLookAndFeel("system")
			utilities.showInfoMessage("Look & Feel Change will take effect after Restart of the Program.")
		self.mylist[index.row()][index.column()]=value
		self.dataChanged.emit(index, index)
		return True

	def flags(self, index):
		if(index.column() == 1):
			return QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
		else:
			return QtCore.Qt.ItemIsEnabled

class LangSettingsDialog(QtGui.QDialog):
	def __init__(self):
		super(LangSettingsDialog, self).__init__()
		self.setWindowTitle('Language Settings - %s' %(getLanguage().getLangName()))

		self.settingsTableModel = LangSettingsTableModel()
		table_view = QtGui.QTableView()
		table_view.setModel(self.settingsTableModel)
		font = QtGui.QFont("Courier New", 14)
		table_view.setFont(font)
		table_view.resizeColumnsToContents()
		table_view.resizeRowsToContents()
		self.mainLayout = QtGui.QVBoxLayout(self)
		self.mainLayout.addWidget(table_view)

		self.setLayout(self.mainLayout)
		self.resize(table_view.size())
		self.exec()

class LangSettingsTableModel(QtCore.QAbstractTableModel):
	def __init__(self):
		super(LangSettingsTableModel, self).__init__()
		self.header = ['Setting', 'Value (Double Click to Edit)']
		self.lang = getLanguage()
		self.mylist = []
		self.refreshMyList()

	def rowCount(self, parent):
		return len(self.mylist)

	def columnCount(self, parent):
		return len(self.mylist[0])

	def headerData(self, col, orientation, role):
		if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
			return self.header[col]
		return None

	def refreshMyList(self):
		self.mylist = [[language.KEYcharSubstitutions, self.lang.getCharSubstitutions()],
		               [language.KEYwordCharRegExp, self.lang.getWordCharRegExp()],
		               [language.KEYmakeCharacterWord, (1 if self.lang.getMakeCharacterWord() else 0)],
		               [language.KEYremoveSpaces, (1 if self.lang.getRemoveSpaces() else 0)],
		               [language.KEYrightToLeft, (1 if self.lang.getRightToLeft() else 0)],
		               [language.KEYfontName, self.lang.getFontName()],
		               [language.KEYfontSize, str(self.lang.getFontSize())],
		               [language.KEYstatusFontName, self.lang.getStatusFontName()],
		               [language.KEYstatusFontSize, str(self.lang.getStatusFontSize())],
		               [language.KEYdictionaryURL1, self.lang.getDictionaryURL1()],
		               [language.KEYwordEncodingURL1, self.lang.getWordEncodingURL1()],
		               [language.KEYopenAutomaticallyURL1, (1 if self.lang.getOpenAutomaticallyURL1() else 0)],
		               [language.KEYdictionaryURL2, self.lang.getDictionaryURL2()],
		               [language.KEYwordEncodingURL2, self.lang.getWordEncodingURL2()],
		               [language.KEYopenAutomaticallyURL2, (1 if self.lang.getOpenAutomaticallyURL2() else 0)],
		               [language.KEYdictionaryURL3, self.lang.getDictionaryURL3()],
		               [language.KEYwordEncodingURL3, self.lang.getWordEncodingURL3()],
		               [language.KEYopenAutomaticallyURL3, (1 if self.lang.getOpenAutomaticallyURL3() else 0)],
		               [language.KEYexportTemplate, self.lang.getExportTemplate()],
		               [language.KEYexportStatuses, self.lang.getExportStatuses()],
		               [language.KEYdoExport, (1 if self.lang.getDoExport() else 0)]]


	def data(self, index, role):
		self.refreshMyList()
		if not index.isValid():
			return None
		elif role == QtCore.Qt.EditRole:
			return self.mylist[index.row()][index.column()]  # node.data method defined above (string)
		elif role != QtCore.Qt.DisplayRole:
			return None
		return self.mylist[index.row()][index.column()]

	def setData(self, index, value, role=QtCore.Qt.DisplayRole):
		if index.column() != 1:
			return False
		row = index.row()
		key = self.mylist[row][0]
		self.lang.putPref(key, str(value))
		self.lang.saveFile()
		self.mylist[index.row()][index.column()]=value
		return True

	def flags(self, index):
		if index.column() == 1:
			return QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
		else:
			return QtCore.Qt.ItemIsEnabled

class NewTextDialog(QtGui.QDialog):
	def __init__(self, text):
		super(NewTextDialog, self).__init__()
		self.setWindowTitle('New %s Text' %(getLanguage().getLangName()))
		mainLayout = QtGui.QVBoxLayout()

		bar1 = QtGui.QHBoxLayout()
		self.textArea = QtGui.QPlainTextEdit()
		self.textArea.setPlainText(text)
		bar1.addWidget(self.textArea)

		mainLayout.addLayout(bar1)

		bar2 = QtGui.QHBoxLayout()
		bar2.addWidget(QtGui.QLabel('Text Name:'))
		self.textName = QtGui.QLineEdit()
		self.textName.setMaxLength(100)
		bar2.addWidget(self.textName)
		mainLayout.addLayout(bar2)

		bar3 = QtGui.QHBoxLayout()
		self.cancelButton = QtGui.QPushButton('Cancel', self)
		self.cancelButton.clicked.connect(self.cancel)
		bar3.addWidget(self.cancelButton)
		self.clearButton = QtGui.QPushButton('Clear Text', self)
		self.clearButton.clicked.connect(self.clear)
		bar3.addWidget(self.clearButton)
		self.pasteButton = QtGui.QPushButton('Paste Clipboard', self)
		self.pasteButton.clicked.connect(self.paste)
		bar3.addWidget(self.pasteButton)
		self.saveButton = QtGui.QPushButton('Save Text', self)
		self.saveButton.clicked.connect(self.save)
		bar3.addWidget(self.saveButton)
		mainLayout.addLayout(bar3)
		self.setLayout(mainLayout)

		#self.readStudyButton.setDefault(True)

		self.setFixedSize(self.width(), self.height())
		self.inSetData = False
		#self.setDataAndPack()
		self.exec()

	def cancel(self):
		self.reject()

	def clear(self):
		self.textArea.clear()

	def paste(self):
		self.textArea.paste()

	def save(self):
		textName = self.textName.text().strip()
		self.textName.setText(textName)
		if not textName:
			utilities.showErrorMessage("Text name not specified.")
			self.textName.setFocus()
			return
		if not utilities.checkFileNameOK(textName):
			utilities.showErrorMessage("Text name contains invalid characters \\, /, :, \", *, ?,\n<, >, |, NEWLINE, TAB or begins with '.'.\nThis has been corrected, please check!")
			self.textName.setText(utilities.replaceNonFileNameCharacters(textName))
			self.textName.setFocus()
			return
		textName = self.textName.text().strip()
		text = self.textArea.toPlainText()
		currMainDir = preferences.getCurrMainDir()
		currLang = preferences.getCurrLang()
		dir = currMainDir
		import os
		if os.path.isdir(dir):
			langdir = os.path.join(dir, '%s%s' %(currLang, constants.TEXT_DIR_SUFFIX))
			if os.path.isdir(langdir):
				langFile = os.path.join(dir, '%s%s' %(currLang, constants.LANG_SETTINGS_FILE_SUFFIX))
				lang = language.Language(langFile)
				setLanguage(lang)
				f = os.path.join(lang.getTextDir(), "%s.txt" %textName)
				if not utilities.createNewFile(f):
					utilities.showErrorMessage("Text Name exists.")
					self.textName.setFocus()
					return
				if constants.EOL not in text:
					text = text.replace(constants.UNIX_EOL, constants.EOL)
				utilities.writeStringIntoFile(f, text)
				utilities.showInfoMessage("Text successfully created:\n%s"%os.path.abspath(f))
				preferences.putCurrText(textName)
		else:
			utilities.showErrorMessage("Not possible.")
		self.accept()
		getStartFrame().setDataAndPack()


class NewLanguageDialog(QtGui.QDialog):
	def __init__(self):
		super(NewLanguageDialog, self).__init__()
		self.setWindowTitle('New Language')
		mainLayout = QtGui.QVBoxLayout()

		bar1 = QtGui.QHBoxLayout()
		bar1.addWidget(QtGui.QLabel('I want to study:'))
		self.comboBoxLanguages = QtGui.QComboBox(self)
		selectItem = ComboBoxItem('[Select...]',1000)
		otherLang = ComboBoxItem('[Other Language]',1000)
		self.comboBoxLanguages.addItem(str(selectItem), selectItem)
		self.comboBoxLanguages.addItem(str(otherLang), otherLang)
		texts = getLangDefs().getTextList()
		for text in texts:
			t = ComboBoxItem(text,1000)
			self.comboBoxLanguages.addItem(str(t), t)
		bar1.addWidget(self.comboBoxLanguages)

		mainLayout.addLayout(bar1)

		bar2 = QtGui.QHBoxLayout()
		bar2.addWidget(QtGui.QLabel('My Native Language:'))
		self.nativeCombo = QtGui.QComboBox(self)

		selectItem = ComboBoxItem('[Select...]',1000)
		otherLang = ComboBoxItem('[Other Language]',1000)
		self.nativeCombo.addItem(str(selectItem), selectItem)
		self.nativeCombo.addItem(str(otherLang), otherLang)
		for text in texts:
			t = ComboBoxItem(text,1000)
			self.nativeCombo.addItem(str(t), t)
		bar2.addWidget(self.nativeCombo)
		mainLayout.addLayout(bar2)

		bar3 = QtGui.QHBoxLayout()
		bar3.addWidget(QtGui.QLabel('Name:'))
		self.langName = NewLangTextEdit(self)
		self.langName.setMaxLength(30)
		bar3.addWidget(self.langName)
		mainLayout.addLayout(bar3)


		bar4 = QtGui.QHBoxLayout()
		self.cancelButton = QtGui.QPushButton('Cancel', self)
		self.cancelButton.clicked.connect(self.cancel)
		bar4.addWidget(self.cancelButton)
		self.createButton = QtGui.QPushButton('Create', self)
		self.createButton.clicked.connect(self.create)
		self.createButton.setEnabled(False)
		bar4.addWidget(self.createButton)
		mainLayout.addLayout(bar4)
		self.setLayout(mainLayout)

		#self.readStudyButton.setDefault(True)

		self.setFixedSize(self.width(), self.height())
		self.inSetData = False
		#self.setDataAndPack()
		#self.exec()
		self.comboBoxLanguages.currentIndexChanged.connect(self.check)
		self.nativeCombo.currentIndexChanged.connect(self.check)

	def cancel(self):
		self.reject()

	def getCbLang1(self):
		return self.nativeCombo

	def getCbLang2(self):
		return self.comboBoxLanguages

	def create(self):
		newLang = self.langName.text().strip()
		if not utilities.checkFileNameOK(newLang):
			utilities.showErrorMessage("Language name contains invalid characters \\, /, :, \", *, ?,\n<, >, |, NEWLINE, TAB or begins with '.'.\nThis has been corrected, please check!")
			self.langName.setText(utilities.replaceNonFileNameCharacters(newLang))
			self.langName.setFocus()
			return
		newLang = self.langName.text().strip()
		l1 = self.getCbLang1().currentIndex() - 2
		l2 = self.getCbLang2().currentIndex() - 2
		currMainDir = preferences.getCurrMainDir()
		fcurrMainDir = currMainDir
		newLangDir = '%s%s'%(newLang,constants.TEXT_DIR_SUFFIX)
		langs = utilities.getSubDirectories(fcurrMainDir)
		notOK = False
		if newLangDir not in langs:
			fnewLangDir = os.path.join(fcurrMainDir, newLangDir)
			if os.path.exists(fnewLangDir):
				notOK = True
			else:
				fTermFile = os.path.join(fcurrMainDir, '%s%s'%(newLang, constants.WORDS_FILE_SUFFIX))
				fLangSettingsFile = os.path.join(fcurrMainDir, '%s%s' %(newLang, constants.LANG_SETTINGS_FILE_SUFFIX))
				if os.path.exists(fTermFile) or os.path.exists(fLangSettingsFile):
					notOK = True
				else:
					try:
						os.mkdir(fnewLangDir)
						ok1 = True
					except OSError as error:
						ok1 = False
					lang = language.Language(fLangSettingsFile)
					l1code = ""
					l1code2 = ""
					if l1 >= 0:
						l1code = getLangDefs().getArray()[l1].getIsoCode().strip()
						l1code2 = l1code
						if len(l1code2) > 2:
							l1code2 = l1code2[:2]
					if l2 >= 0:
						ld2 = getLangDefs().getArray()[l2]
						if ld2.isBiggerFont():
							lang.putPref(language.KEYfontSize,str(((lang.getFontSize() * 3) / 2)))
						if ld2.getWordCharRegExp().strip() != "":
							lang.putPref(language.KEYwordCharRegExp, ld2.getWordCharRegExp().strip())
						lang.putPref(language.KEYmakeCharacterWord, 1 if ld2.isMakeCharacterWord() else 0)
						lang.putPref(language.KEYremoveSpaces,  1 if ld2.isRemoveSpaces() else 0)
						lang.putPref(language.KEYrightToLeft,  1 if ld2.isRightToLeft() else 0)
						l2code = ld2.getIsoCode().strip()
						if len(l2code) > 2:
							l2code = l2code[:2]
						if l1code != "" and l2code != "":
							lang.putPref(language.KEYdictionaryURL1,"http://translate.google.com/?ie=UTF-8&sl=%s&t;=%s&text=###" %(l2code, l1code))
							lang.putPref(language.KEYdictionaryURL2,"http://glosbe.com/%s/%s/###" %(l2code, l1code2))
							if ld2.isTtsAvailable():
								lang.putPref(language.KEYdictionaryURL3,"http://translate.google.com/translate_tts?ie=UTF-8&tl=%s&q=###" %l2code)
						lang.saveFile()
					else:
						if l1code != "":
							lang.putPref(language.KEYdictionaryURL1,"http://translate.google.com/?ie=UTF-8&sl=auto&tl=%s&text=###" %l1code)
							lang.saveFile()
					setLanguage(lang)
					ok2 = os.path.exists(fLangSettingsFile)
					ok3 = utilities.createEmptyFile(fTermFile)
					if (ok1 and ok2 and ok3):
						utilities.showInfoMessage("Language '%s' successfully created.\n\n"
						                          "Please put your texts into the directory\n"
						                          "%s."
						                          "\n\nThe vocabulary will be saved in\n"
						                          "%s." %(newLang, os.path.abspath(fnewLangDir), os.path.abspath(fTermFile)))
						preferences.putCurrLang(newLang)
						getStartFrame().setDataAndPack()
						self.accept()
					else:
						utilities.showErrorMessage("Language '%s' NOT successfully created."
						                           "\n\nPlease check %s"
						                           " directory.") %(newLang, constants.SHORT_NAME)
		else:
			notOK = True
		if notOK:
			utilities.showErrorMessage("Creation of language '%s' NOT possible,\n"
			                           "directory or file(s) already exist.\n\nPlease check %s"
			                           " directory." %(newLang, constants.SHORT_NAME))

	def getSelectedLanguage(self):
		return self.comboBoxLanguages.itemData(self.comboBoxLanguages.currentIndex()).getText()

	def check(self):
		l1 = self.getCbLang1().currentIndex()
		l2 = self.getCbLang2().currentIndex()
		text = self.langName.text().strip()
		enableButton = (l1 > 0) and (l2 > 0) and (text != '')
		if (enableButton and (l1 == l2)):
			if (l1 > 1):
				enableButton = False
		self.createButton.setEnabled(enableButton)

class NewLangTextEdit(QtGui.QLineEdit):
	def __init__(self, parent):
		super(NewLangTextEdit, self).__init__()
		self.parent = parent

	def focusInEvent(self, QFocusEvent):
		l2 = self.parent.getCbLang2().currentIndex()
		if l2 > 1 and self.text().strip() == '':
			selectLang = self.parent.getSelectedLanguage()
			self.setText(selectLang)
			self.parent.check()