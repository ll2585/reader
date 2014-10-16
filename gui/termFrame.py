import gui.utilities as utilities
import app.constants as constants
import gui.preferences as preferences
from app.terms import Term, RootWord
import gui.application
from app.TermStatus import TermStatus as TermStatus
from PyQt4 import QtGui, QtCore

class TermFrame(QtGui.QMainWindow):
	def __init__(self):
		import functools
		super(TermFrame, self).__init__()
		self.setWindowTitle('Term')
		self.originalKey = ''
		self.mainPanel = QtGui.QFrame()

		mainLayout = QtGui.QVBoxLayout()
		#mainLayout.setContentsMargins(5)
		self.mainPanel.setLayout(mainLayout)
		#self.mainPanel.setStyleSheet("border:5px; ")
		formLayout = QtGui.QFormLayout()
		bar1 = QtGui.QHBoxLayout()
		#bar1.addWidget(QtGui.QLabel('Term:'))
		self.tfTerm = MultiLineTextField('', 200, 2, 35, self)
		#bar1.addWidget(self.tfTerm.getTextAreaScrollPane())
		formLayout.addRow(QtGui.QLabel('Term:'), self.tfTerm.getTextAreaScrollPane())
		self.tfRootTerm = MultiLineTextField('', 200, 2, 35, self)
		formLayout.addRow(QtGui.QLabel('Root Term:'), self.tfRootTerm.getTextAreaScrollPane())
		self.tfRootTerm.addTextChangedEvent(self.rootEditted)
		self.tfDefinition = MultiLineTextField('', 200, 4, 35, self)
		formLayout.addRow(QtGui.QLabel('Root Definition:'), self.tfDefinition.getTextAreaScrollPane())
		self.tfTranslation = MultiLineTextField('', 200, 4, 35, self)
		formLayout.addRow(QtGui.QLabel('Translation:'), self.tfTranslation.getTextAreaScrollPane())
		langName = gui.application.getLanguage().getLangName()
		if langName == 'Korean':
			lookupLayout = QtGui.QHBoxLayout()

			self.naverButton = QtGui.QPushButton("Lookup on Naver")
			self.naverButton.clicked.connect(functools.partial(self.lookupButtonClicked, langName, False))
			lookupLayout.addWidget(self.naverButton)

			self.naverRootButton = QtGui.QPushButton("Lookup Root on Naver")
			self.naverRootButton.clicked.connect(functools.partial(self.lookupButtonClicked, langName, True))
			lookupLayout.addWidget(self.naverRootButton)

			formLayout.addRow(QtGui.QLabel('Lookup:'), lookupLayout)
		self.tfSentence = MultiLineTextField('', 400, 2, 35, self)
		formLayout.addRow(QtGui.QLabel('Sentence:'), self.tfSentence.getTextAreaScrollPane())
		bar1.addLayout(formLayout)
		mainLayout.addLayout(bar1)
		'''
		bar2 = QtGui.QHBoxLayout()
		bar2.addWidget(QtGui.QLabel('Root Term:'))
		self.tfRootTerm = MultiLineTextField('', 200, 2, 35, self)
		bar2.addWidget(self.tfRootTerm.getTextAreaScrollPane())
		mainLayout.addLayout(bar2)

		bar3 = QtGui.QHBoxLayout()
		bar3.addWidget(QtGui.QLabel('Translation:'))
		self.tfTranslation = MultiLineTextField('', 200, 2, 35, self)
		bar3.addWidget(self.tfTranslation.getTextAreaScrollPane())
		mainLayout.addLayout(bar3)

		bar4 = QtGui.QHBoxLayout()
		bar4.addWidget(QtGui.QLabel('Sentence:'))
		self.tfSentence = MultiLineTextField('', 400, 2, 35, self)
		bar4.addWidget(self.tfSentence.getTextAreaScrollPane())
		mainLayout.addLayout(bar4)
		'''
		bar5 = QtGui.QHBoxLayout()
		bar5.setSpacing (10)
		bar5.addStretch()
		bar5.addWidget(QtGui.QLabel('Status:'))
		self.rbStatus = []
		bgStatus = QtGui.QButtonGroup()
		#-2 because i have 9 because of 8 ids and 1 color group
		for i in range(len(TermStatus)-1):
			self.rbStatus.append(QtGui.QRadioButton(str(i + 1)))
			#rbStatus[i].addActionListener(listener);
			bgStatus.addButton(self.rbStatus[i])
			bar5.addWidget(self.rbStatus[i])
				#, "gapbottom 10px"
				#	+ (i == 0 ? ", split"
				#			: (i == (rbStatus.length - 1) ? ", wrap" : "")));
		self.rbStatus[5].setText("Ign")
		self.rbStatus[6].setText("WKn")

		mainLayout.addLayout(bar5)

		bar6 = QtGui.QHBoxLayout()
		self.butDelete = QtGui.QPushButton("Delete")
		bar6.addWidget(self.butDelete)
		lang = gui.application.getLanguage()

		self.butLookup1 = QtGui.QPushButton("Dict1")
		self.butLookup1.setEnabled(lang.getDictionaryURL1().startswith(constants.URL_BEGIN))
		self.butLookup1.clicked.connect(functools.partial(self.lookupDict, 1))
		bar6.addWidget(self.butLookup1)

		self.butLookup2 = QtGui.QPushButton("Dict2")
		self.butLookup2.setEnabled(lang.getDictionaryURL2().startswith(constants.URL_BEGIN))
		self.butLookup2.clicked.connect(functools.partial(self.lookupDict, 2))
		bar6.addWidget(self.butLookup2)

		self.butLookup3 = QtGui.QPushButton("Dict3")
		self.butLookup3.setEnabled(lang.getDictionaryURL3().startswith(constants.URL_BEGIN))
		self.butLookup3.clicked.connect(functools.partial(self.lookupDict, 3))
		bar6.addWidget(self.butLookup3)

		self.butSave = QtGui.QPushButton("Save")
		self.butSave.clicked.connect(self.save)
		bar6.addWidget(self.butSave)

		mainLayout.addLayout(bar6)
		mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

		self.butSave.setDefault(True)


		self.setCentralWidget(self.mainPanel)

		#d = QtGui.QDesktopWidget.screenGeometry()
		self.inSetData = False
		self.adjustSize()
		self.rootChangedBool = False
		self.originalRoot = ''
		self.originalDef = ''
		self.originalTrans = ''
		self.originalStatus = None

	def lookupNaver(self, root):
		from app.koreanHelper import get_root, get_root_korean
		if not root:
			word = utilities.replaceControlCharactersWithSpace(self.getTfTerm().getTextArea().toPlainText())
		else:
			word =  utilities.replaceControlCharactersWithSpace(self.getTfRootTerm().getTextArea().toPlainText())
		result = get_root(word)
		if(result):
			self.tfRootTerm.getTextArea().setText(result[0][0])
			self.tfTranslation.getTextArea().setText(result[1])
		else:
			self.tfRootTerm.getTextArea().setText('Please Manually Enter')
		kor_def = get_root_korean(word)
		if(kor_def):
			self.tfDefinition.getTextArea().setText(kor_def[1])
			if not result:
				self.tfRootTerm.getTextArea().setText(kor_def[0])
		else:
			self.tfDefinition.getTextArea().setText('Please Manually Enter')

	def lookupButtonClicked(self, lang, root = False):
		lookup = {'Korean': self.lookupNaver}
		lookup[lang](root)


	def rootEditted(self):
		self.rootChangedBool = self.getTfRootTerm().getTextArea().toPlainText() != self.originalRoot

	def rootChanged(self):
		if self.rootChangedBool:
			terms = gui.application.getTerms()
			editRoot = self.getTfRootTerm().getTextArea().toPlainText()
			newRoot = editRoot
			if newRoot in terms.rootDict:
				newRootTerm = terms.rootDict[newRoot]
				self.tfDefinition.getTextArea().setText(newRootTerm.definition)
				self.tfTranslation.getTextArea().setText(newRootTerm.translation)
				self.setRbStatus(newRootTerm.status)
			self.rootChangedBool = False

	def startNew(self, term, sentence):
		#utilities.setComponentOrientation(tfTerm.getTextArea());
		#utilities.setComponentOrientation(tfSentence.getTextArea());
		#utilities.setComponentOrientation(cbSimilar);
		self.tfSentence.getTextArea().setTextColor(QtCore.Qt.black)
		self.setWindowTitle("New Term")
		self.originalKey = term.lower()
		self.tfTerm.getTextArea().setText(term)
		self.tfTranslation.getTextArea().setText("")
		self.tfRootTerm.getTextArea().setText('')
		self.tfDefinition.getTextArea().setText('')
		self.originalRoot = ''
		self.originalDef = ''
		self.originalTrans = ''
		self.originalStatus = TermStatus.Unknown


		if not preferences.getCurrText() == "<Vocabulary>":
			self.tfSentence.getTextArea().setText(sentence)
		else:
			self.tfSentence.getTextArea().setText("")
		self.setRbStatus(TermStatus.Unknown)

		self.adjustSize()
		self.setVisible(True)
		self.tfTranslation.getTextArea().setFocus()

	def startEdit(self, term, sentence):
		#utilities.setComponentOrientation(tfTerm.getTextArea());
		#utilities.setComponentOrientation(tfSentence.getTextArea());
		#utilities.setComponentOrientation(cbSimilar);
		self.tfSentence.getTextArea().setTextColor(QtCore.Qt.black)
		self.setWindowTitle("Edit Term")
		self.originalKey = term.getKey()
		self.tfTerm.getTextArea().setText(term.getTerm())
		self.tfRootTerm.getTextArea().setText(term.root.word)
		self.originalRoot = term.root.word
		self.tfDefinition.getTextArea().setText(term.root.definition)
		self.tfTranslation.getTextArea().setText(term.getTranslation())

		self.originalDef = term.root.definition
		self.originalTrans = term.getTranslation()
		self.originalStatus = term.getStatus()

		if not preferences.getCurrText() == "<Vocabulary>":
			self.tfSentence.getTextArea().setText(sentence)
		else:
			self.tfSentence.getTextArea().setText("")
		self.setRbStatus(term.getStatus())

		self.adjustSize()
		self.setVisible(True)
		self.tfTranslation.getTextArea().setFocus()

	def setRbStatus(self, ts):
		index = ts.ordinal() - 1
		count = 0
		for i in range(len(self.rbStatus)):
			self.rbStatus[i].setChecked(i == index)
			if i == index:
				count += 1

		if count == 0:
			self.rbStatus[0].setChecked(True)


	def lookupDict(self, i):
		gui.application.getLanguage().lookupWordInBrowser(utilities.replaceControlCharactersWithSpace(self.getTfTerm().getTextArea().toPlainText()), i, True)

	def getTfTerm(self):
		return self.tfTerm

	def getTfRootTerm(self):
		return self.tfRootTerm

	def getTfTranslation(self):
		return self.tfTranslation

	def getTfSentence(self):
		return self.tfSentence

	def getTfDefinition(self):
		return self.tfDefinition

	def getOriginalKey(self):
		return self.originalKey

	def getRbStatus(self):
		for i in range(len(self.rbStatus)):
			if (self.rbStatus[i].isChecked()):
				return TermStatus.getStatusFromOrdinal((i + 1))
		return TermStatus.Unknown

	def save(self):
		term = utilities.replaceControlCharactersWithSpace(self.getTfTerm().getTextArea().toPlainText())
		root = utilities.replaceControlCharactersWithSpace(self.getTfRootTerm().getTextArea().toPlainText())
		definition = self.tfDefinition.getTextArea().toPlainText()
		translation = utilities.replaceControlCharactersWithSpace(self.getTfTranslation().getTextArea().toPlainText())
		sentence = utilities.replaceControlCharactersWithSpace(self.getTfSentence().getTextArea().toPlainText())
		priorSentence = ''
		sentenceCLOZE = ''
		followingSentence = ''
		source = ''
		status = self.getRbStatus()

		if term == (""):
			utilities.showErrorMessage("Mandatory field.\nTerm must not be empty.")
			self.getTfTerm().getTextArea().setFocus(True)
			return

		if status != TermStatus.Ignored and status != TermStatus.WellKnown:
			if translation == "":
				utilities.showErrorMessage("Mandatory field.\nTranslation must not be empty, unless status is 'Ignored' or 'Well Known'.");
				self.getTfTranslation().getTextArea().setFocus(True)
				return
		key = term.lower()
		changedTerm = self.getOriginalKey() != key
		changedRoot = self.getTfRootTerm().getTextArea().toPlainText() != self.originalRoot and self.originalRoot != ''
		terms = gui.application.getTerms()
		t = terms.getTermFromKey(key)
		exists = (t != None)
		if root not in terms.rootDict:
			newID = len(terms.rootDict)+1
			#(self, id, word, definition, translation, priorSentence, sentenceCLOZE, sentence, followingSentence, source, status, new = True, updated = False):
			rootTerm = RootWord(newID, root, definition, translation, 'prior sentence TODO', 'sentenceCLOZETODO', sentence, 'followingsentenceTODO', 'sourceTODO', status.getStatusCode(), new=True, updated=False)
			terms.rootDict[root] = rootTerm
		else:
			rootTerm = terms.rootDict[root]
			if definition != rootTerm.definition or translation != rootTerm.translation or status != rootTerm.status:
				if not utilities.showYesNoQuestion(
					"You have changed the Root Term definition or translation!\n\nAre you sure?", True):
					return
				rootTerm.definition = definition
				rootTerm.translation = translation
				rootTerm.status = status
				rootTerm.updated = True
		if not exists:
			if changedTerm:
				if not utilities.showYesNoQuestion(
						"You have changed the Term from\n[%s] to the NEW Term [%s].\n\nAre you sure?" %(self.getOriginalKey(), key), True):
					return
			if changedRoot:
				if not utilities.showYesNoQuestion(
						"You have changed the Root from\n[%s] to the NEW Root [%s].\n\nAre you sure?" %(self.originalRoot, self.getTfRootTerm().getTextArea().toPlainText()), True):
					return
			#self, word, definition, translation, priorSentence, sentenceCLOZE, sentence, followingSentence, source, status
			#terms.addTerm(Term(term, RootWord(root, definition, translation, priorSentence, sentenceCLOZE, sentence, followingSentence, source, status.getStatusCode())))
			newTerm = Term(term, terms.nextID(), rootTerm, rootTerm.id, True, False)
			terms.addTerm(newTerm)
		else:
			if (changedTerm):
				if not utilities.showYesNoQuestion(
								"You have changed the Term from\n[%s] to the EXISTENT Term [%s].\n\nAre you sure to OVERWRITE?" %(self.getOriginalKey(), key),
								False):
					return
			if changedRoot:
				if not utilities.showYesNoQuestion(
						"You have changed the Root from\n[%s] to the EXISTENT Root [%s].\n\nAre you sure?" %(self.originalRoot, self.getTfRootTerm().getTextArea().toPlainText()), True):
					return
				t.updated = True
			t.setTerm(term)
			t.setTranslation(translation)
			t.setSentence(sentence)
			t.setStatus(status)
			t.updated = True
			terms.setDirty(True)
		self.setVisible(False)
		gui.application.getText().matchWithTerms()
		gui.application.getTextFrame().getTextPanel().update()
		gui.application.getTextFrame().getTextPanel().setFocus(True)


class MultiLineTextField():
	def __init__(self, text, maxChar, lines, width, frame):
		self.textArea = customEdit(frame)
		self.setHeight(lines)
		self.textArea.setLineWrapColumnOrWidth(width)
		self.textAreaScrollPane = QtGui.QScrollArea()

		self.textAreaScrollPane.setWidgetResizable(False)

		self.textAreaScrollPane.setWidget(self.textArea)
		self.textAreaScrollPane.adjustSize()
		self.textAreaScrollPane.resize(self.textArea.size())

	def getTextAreaScrollPane(self):
		return self.textAreaScrollPane

	def getTextArea(self):
		return self.textArea

	def setHeight(self, rows):
		m = self.textArea.fontMetrics()
		rowHeight = m.lineSpacing()
		self.textArea.setFixedHeight(rowHeight * rows)

	def addTextChangedEvent(self, callback):
		self.textArea.textChanged.connect(callback)
		self.textArea.event = True

class customEdit(QtGui.QTextEdit):
	def __init__(self, par):
		QtGui.QTextEdit.__init__(self)
		self.parent = par

	def focusOutEvent(self, e):
		QtGui.QTextEdit.focusOutEvent(self,e)
		if(self.event):
			self.parent.rootChanged()