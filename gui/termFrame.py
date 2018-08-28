import gui.utilities as utilities
import app.constants as constants
import gui.preferences as preferences
from app.terms import Term, Lemma
import gui.application
from app.TermStatus import TermStatus as TermStatus
import sip
sip.setapi('QString', 2)
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

		self.term_text = QtGui.QLabel()
		self.copy_term_button = QtGui.QPushButton("Copy Term")
		self.copy_term_button.clicked.connect(self.copy_term)
		term_layout = QtGui.QHBoxLayout()
		term_layout.addWidget(self.term_text)
		term_layout.addWidget(self.copy_term_button)
		formLayout.addRow(QtGui.QLabel('Term:'), term_layout)

		#TODO: allow for deleting and saving the changes and also event triggering the button
		lemma_layout = QtGui.QHBoxLayout()
		self.new_lemma_button = QtGui.QPushButton("Add new")
		self.new_lemma_button.clicked.connect(self.edit_lemma)
		self.delete_lemma_button = QtGui.QPushButton("Remove lemma from term")
		self.delete_lemma_button.clicked.connect(self.remove_lemma)
		self.lemma_dropdown = QtGui.QComboBox(self)
		self.lemma_dropdown.currentIndexChanged.connect(self.lemma_changed)
		self.lemma_text_field = MultiLineTextField('', 200, 2, 35, self)
		self.lemma_text_field.addTextChangedEvent(self.lemma_edited)
		self.lemma_widget_stack = StackedWidget()

		self.lemma_widget_stack.addWidget(self.lemma_text_field.getTextAreaScrollPane())
		self.lemma_widget_stack.addWidget(self.lemma_dropdown)
		lemma_layout.addWidget(self.lemma_widget_stack)
		lemma_layout.addWidget(self.new_lemma_button)
		lemma_layout.addWidget(self.delete_lemma_button)
		formLayout.addRow(QtGui.QLabel('Lemma:'), lemma_layout)

		self.tfRootTerm = MultiLineTextField('', 200, 2, 35, self)
		formLayout.addRow(QtGui.QLabel('Root Term:'), self.tfRootTerm.getTextAreaScrollPane())
		self.tfRootTerm.addTextChangedEvent(self.lemma_edited)
		self.definition_text_field = MultiLineTextField('', 200, 4, 35, self)
		self.definition_dropdown = QtGui.QComboBox(self)
		definition_row = QtGui.QHBoxLayout()
		definition_row.addWidget(self.definition_text_field.getTextAreaScrollPane())
		definition_row.addWidget(self.definition_dropdown)
		formLayout.addRow(QtGui.QLabel('Lemma Definition:'), definition_row)
		self.tfTranslation = MultiLineTextField('', 200, 4, 35, self)
		formLayout.addRow(QtGui.QLabel('Translation:'), self.tfTranslation.getTextAreaScrollPane())
		lang_name = gui.application.getLanguage().getLangName()
		if lang_name == 'Korean':
			lookupLayout = QtGui.QHBoxLayout()

			self.naver_button = QtGui.QPushButton("Lookup on Naver")
			self.naver_button.clicked.connect(functools.partial(self.lookup_button_clicked, lang_name, False))
			lookupLayout.addWidget(self.naver_button)

			self.naver_lemma_button = QtGui.QPushButton("Lookup Lemma on Naver")
			self.naver_lemma_button.clicked.connect(functools.partial(self.lookup_button_clicked, lang_name, True))
			lookupLayout.addWidget(self.naver_lemma_button)

			formLayout.addRow(QtGui.QLabel('Lookup:'), lookupLayout)
		self.tfSentence = MultiLineTextField('', 400, 5, 35, self)
		formLayout.addRow(QtGui.QLabel('Sentence:'), self.tfSentence.getTextAreaScrollPane())
		self.notes_text_field = MultiLineTextField('', 400, 5, 35, self)
		formLayout.addRow(QtGui.QLabel('Notes:'), self.notes_text_field.getTextAreaScrollPane())
		bar1.addLayout(formLayout)
		mainLayout.addLayout(bar1)

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
		self.rbStatus[5].setText("Ign")
		self.rbStatus[6].setText("WKn")

		mainLayout.addLayout(bar5)

		bar6 = QtGui.QHBoxLayout()
		self.butDelete = QtGui.QPushButton("Delete")
		bar6.addWidget(self.butDelete)
		lang = gui.application.getLanguage()

		self.butLookup1 = QtGui.QPushButton("Dict1")
		self.butLookup1.setEnabled(lang.get_dictionary_url_1().startswith(constants.URL_BEGIN))
		self.butLookup1.clicked.connect(functools.partial(self.lookupDict, 1))
		bar6.addWidget(self.butLookup1)

		self.butLookup2 = QtGui.QPushButton("Dict2")
		self.butLookup2.setEnabled(lang.get_dictionary_url_2().startswith(constants.URL_BEGIN))
		self.butLookup2.clicked.connect(functools.partial(self.lookupDict, 2))
		bar6.addWidget(self.butLookup2)

		self.butLookup3 = QtGui.QPushButton("Dict3")
		self.butLookup3.setEnabled(lang.get_dictionary_url_3().startswith(constants.URL_BEGIN))
		self.butLookup3.clicked.connect(functools.partial(self.lookupDict, 3))
		bar6.addWidget(self.butLookup3)

		self.butSave = QtGui.QPushButton("Save")
		self.butSave.clicked.connect(self.save)
		bar6.addWidget(self.butSave)

		mainLayout.addLayout(bar6)
		mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

		self.butSave.setDefault(True)


		self.setCentralWidget(self.mainPanel)
		self.setFixedSize(self.mainPanel.sizeHint())


		#d = QtGui.QDesktopWidget.screenGeometry()
		self.inSetData = False
		self.adjustSize()
		self.is_lemma_changed = False
		self.original_lemma = ''
		self.originalDef = ''
		self.originalTrans = ''
		self.originalStatus = None
		self.selected_lemma = None
		self.selected_lemma_id = -99
		self.term = None
		self.sentence = ''
		self.term_id = -99

	def copy_term(self):
		clipboard = QtGui.QApplication.clipboard()
		clipboard.setText(self.term_text.text())

	def lemma_changed(self):
		if self.selected_lemma_id > 0 and self.lemma_dropdown.currentText() != '':
			terms = gui.application.getTerms()
			self.selected_lemma = terms.real_lemma_dict[self.lemma_dropdown.currentText()][0]
			self.selected_lemma_id = self.selected_lemma.id
			self.set_lemma_fields()

	def remove_lemma(self):
		terms = gui.application.getTerms()
		if len(self.term.possible_lemmas) > 1:
			for index, lemma_link in enumerate(self.term.possible_lemmas):
				if lemma_link['lemma_id'] == self.selected_lemma_id:
					terms.add_removed_link(self.term.id, self.selected_lemma_id)
					self.lemma_dropdown.removeItem(self.lemma_dropdown.currentIndex())
					del self.term.possible_lemmas[index]
					break
		elif len(self.term.possible_lemmas) == 1:
			terms.add_removed_link(self.term.id, self.selected_lemma_id)
			self.lemma_dropdown.removeItem(self.lemma_dropdown.currentIndex())
			del self.term.possible_lemmas[0]
			self.prepare_for_new_lemma(self.sentence)
		else:
			self.prepare_for_new_lemma(self.sentence)

	#TODO: finish refactoring this...or getting it to work
	def lookup_naver(self, lemma):
		from app.koreanHelper import get_lemma, get_lemma_korean
		if not lemma:
			word = utilities.replaceControlCharactersWithSpace(self.term_text.text())
		else:
			if self.selected_lemma_id == -1:
				word = utilities.replaceControlCharactersWithSpace(self.lemma_text_field.getTextArea().toPlainText())
			else:
				word =  utilities.replaceControlCharactersWithSpace(self.selected_lemma.word)
		result = get_lemma(word)

		if result:
			self.lemma_text_field.getTextArea().setText(result[0][0])
			self.tfTranslation.getTextArea().setText(result[1])
		else:
			self.lemma_text_field.getTextArea().setText('Please Manually Enter')
		kor_def = get_lemma_korean(word)
		print(kor_def)
		if(kor_def):
			self.definition_text_field.getTextArea().setText(kor_def[1])
			if not result:
				self.lemma_text_field.getTextArea().setText(kor_def[0])
				eng_def_using_korean_lemma = get_lemma(kor_def[0])
				if eng_def_using_korean_lemma:
					self.tfTranslation.getTextArea().setText(eng_def_using_korean_lemma[1])
			self.lemma_was_changed()
		else:
			self.definition_text_field.getTextArea().setText('Please Manually Enter')


	def lookup_button_clicked(self, lang, lemma = False):
		lookup = {'Korean': self.lookup_naver}
		lookup[lang](lemma)


	def lemma_edited(self):
		new_lemma_text = self.lemma_text_field.getTextArea().toPlainText()
		if new_lemma_text != '':
			self.is_lemma_changed = new_lemma_text != self.original_lemma

	def lemma_was_changed(self):
		if self.is_lemma_changed:
			new_lemma_text = self.lemma_text_field.getTextArea().toPlainText()
			terms = gui.application.getTerms()
			new_lemma = new_lemma_text
			if new_lemma_text == '':
				self.definition_text_field.getTextArea().setText('')
				self.tfTranslation.getTextArea().setText('')
			elif self.lemma_exists(new_lemma_text):
				try:
					self.selected_lemma = self.get_lemma_from_string(new_lemma_text)
				except TypeError:
					print(":ERROR: {0}".format(new_lemma_text))
				self.selected_lemma_id = self.selected_lemma.id
				self.set_lemma_fields()
		if self.lemma_text_field.getTextArea().toPlainText() == '' and self.selected_lemma.word == '':
			self.prepare_for_new_lemma(self.sentence)

	def startNew(self, term, sentence):
		#utilities.setComponentOrientation(tfSentence.getTextArea());
		#utilities.setComponentOrientation(cbSimilar);
		self.term = term
		self.term_id = -1
		self.sentence = sentence
		self.tfSentence.getTextArea().setTextColor(QtCore.Qt.black)
		self.prepare_for_new_lemma(sentence)
		self.setWindowTitle("New Term")
		self.originalKey = term.lower()
		self.term_text.setText(term)
		self.original_lemma = ''
		self.originalDef = ''
		self.originalTrans = ''
		self.originalStatus = TermStatus.Unknown
		self.notes_text_field.getTextArea().setText("")

		if not preferences.getCurrText() == "<Vocabulary>":
			self.tfSentence.getTextArea().setText(sentence)
		else:
			self.tfSentence.getTextArea().setText("")
		self.setRbStatus(TermStatus.Unknown)

		self.adjustSize()
		self.setVisible(True)
		self.lemma_text_field.getTextArea().setFocus()

	def set_lemma_fields(self):
		if self.selected_lemma:
			self.tfRootTerm.getTextArea().setText(self.selected_lemma.word)
			self.original_lemma = self.selected_lemma.word
			self.definition_text_field.getTextArea().setText(self.selected_lemma.definition)
			self.tfTranslation.getTextArea().setText(self.selected_lemma.translation)
			self.setRbStatus(self.selected_lemma.status)
			self.notes_text_field.getTextArea().setText("")
			self.originalDef = self.selected_lemma.definition
			self.originalTrans = self.selected_lemma.translation
			self.originalStatus = self.selected_lemma.status
			if not preferences.getCurrText() == "<Vocabulary>":
				self.tfSentence.getTextArea().setText(self.sentence)
				if type(self.term) == Term:
					self.notes_text_field.getTextArea().setText(self.term.get_notes_of_lemma_id(self.selected_lemma_id))
			else:
				self.tfSentence.getTextArea().setText("")

	def prepare_for_new_lemma(self, sentence):
		self.lemma_widget_stack.setCurrentWidget(self.lemma_text_field.getTextAreaScrollPane())
		# TODO: add in sentencecloze, prior sentence, following sentence, source
		self.selected_lemma = Lemma(-1, '', '', '', '', '', sentence, '', '', 1)
		self.selected_lemma_id = -1
		self.lemma_text_field.getTextArea().setText('')
		self.lemma_dropdown.clear()
		self.tfTranslation.getTextArea().setText("")
		self.tfRootTerm.getTextArea().setText('')
		self.definition_text_field.getTextArea().setText('')
		self.tfSentence.getTextArea().setText(sentence)

	def startEdit(self, term, sentence):
		terms = gui.application.getTerms()
		self.term = term
		self.term_text.setText(term.get_term())
		self.term_id = term.id
		self.sentence = sentence
		#utilities.setComponentOrientation(tfSentence.getTextArea());
		#utilities.setComponentOrientation(cbSimilar);
		self.tfSentence.getTextArea().setTextColor(QtCore.Qt.black)
		self.setWindowTitle("Edit Term")
		self.originalKey = term.getKey()
		self.notes_text_field.getTextArea().setText("")
		if len(term.get_possible_lemmas())==0:
			self.prepare_for_new_lemma(sentence)
			self.lemma_text_field.getTextArea().setFocus()
		else:
			self.lemma_text_field.getTextArea().setText('')
			self.lemma_dropdown.clear()
			self.lemma_widget_stack.setCurrentIndex(1)
			for t in term.get_possible_lemmas():
				self.lemma_dropdown.addItem(terms.lemma_id_dict[t].word)
			# TODO: find a way to change the default - right now defaults to the first result of the lemma
			try:
				self.selected_lemma = terms.real_lemma_dict[self.lemma_dropdown.currentText()][0]
			except TypeError:
				print(self.lemma_dropdown.currentText())
			self.selected_lemma_id = self.selected_lemma.id
			#TODO: get this to work (adding new definitions)
			self.definition_dropdown.addItem("1")
			self.definition_dropdown.addItem("Add New Definition")
			self.set_lemma_fields()
			self.tfTranslation.getTextArea().setFocus()
		self.setRbStatus(self.term.get_status())

		self.adjustSize()
		self.setVisible(True)



	def edit_lemma(self):
		#TODO: allow to go back? right now no going back
		self.selected_lemma = self.selected_lemma.new_empty_lemma()
		self.prepare_for_new_lemma(self.sentence)
		self.selected_lemma_id = self.selected_lemma.id
		self.lemma_changed()


	def lemma_exists(self, string):
		terms = gui.application.getTerms()
		return string in terms.real_lemma_dict

	def get_lemma_from_string(self, string):
		terms = gui.application.getTerms()
		#TODO: dont always return the first one
		return terms.real_lemma_dict[string][0]


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
		return self.definition_text_field

	def getOriginalKey(self):
		return self.originalKey

	def getRbStatus(self):
		for i in range(len(self.rbStatus)):
			if (self.rbStatus[i].isChecked()):
				return TermStatus.getStatusFromOrdinal((i + 1))
		return TermStatus.Unknown

	def save(self):
		term_text = utilities.replaceControlCharactersWithSpace(self.term_text.text())
		if self.is_lemma_changed:
			lemma_text = utilities.replaceControlCharactersWithSpace(self.lemma_text_field.getTextArea().toPlainText())
		else:
			lemma_text = self.selected_lemma.word
		definition = self.definition_text_field.getTextArea().toPlainText()
		translation = utilities.replaceControlCharactersWithSpace(self.getTfTranslation().getTextArea().toPlainText())
		sentence = utilities.replaceControlCharactersWithSpace(self.getTfSentence().getTextArea().toPlainText())
		notes = utilities.replaceControlCharactersWithSpace(self.notes_text_field.getTextArea().toPlainText())
		priorSentence = ''
		sentenceCLOZE = ''
		followingSentence = ''
		source = ''
		status = self.getRbStatus()

		term_id = self.term_id
		lemma_id = self.selected_lemma_id
		language = gui.application.getLanguage().getLangName()

		if status != TermStatus.Ignored and status != TermStatus.WellKnown:
			if translation == "":
				utilities.showErrorMessage("Mandatory field.\nTranslation must not be empty, unless status is 'Ignored' or 'Well Known'.");
				self.getTfTranslation().getTextArea().setFocus(True)
				return

		changed_lemma = self.is_lemma_changed and self.original_lemma != ''
		terms = gui.application.getTerms()
		is_new_term = self.term_id == -1
		#check for new lemma first
		if self.selected_lemma_id == -1:
			new_lemma_id = terms.get_next_lemma_id_and_increment()
			#(self, id, word, definition, translation, priorSentence, sentenceCLOZE, sentence, followingSentence, source, status, new = True, updated = False):
			lemma_id = new_lemma_id
			lemma = Lemma(new_lemma_id, lemma_text, definition, translation, 'prior sentence TODO', 'sentenceCLOZETODO', sentence, 'followingsentenceTODO', 'sourceTODO', status.getStatusCode(), new=True, updated=False)
			#TODO: move this shit to terms
			terms.real_lemma_dict[lemma_text] = new_lemma_id
			terms.lemma_id_dict[new_lemma_id] = lemma
			terms.lemma_dict[lemma_text] = lemma
			terms.setDirty(True)
		else:
			lemma = terms.lemma_id_dict[self.selected_lemma_id]
			if definition != lemma.definition or translation != lemma.translation or status != lemma.status:
				#got rid of this because duh...
				#if not utilities.showYesNoQuestion(
				#	"You have changed the Root Term definition or translation or status!\n\nAre you sure?", True):
				#	return
				#TODO: maybe make setters
				lemma.definition = definition
				lemma.translation = translation
				lemma.status = status
				lemma.updated = True
				terms.setDirty(True)
		if is_new_term:
			next_term_id = terms.get_next_term_id_and_increment()
			term_id = next_term_id
			term = Term(term_text, next_term_id, lemma_text, lemma_id, True, False)
			terms.add_term(term)
			#TODO: move this shit to terms
			terms.real_term_dict[lemma] = term
			terms.term_id_dict[next_term_id] = term
			terms.setDirty(True)
		else:
			term = terms.term_id_dict[term_id]
		if term.didnt_originally_have_lemma(lemma_id):
			print("adding lemma {0} to {1}".format(lemma_id, term_id))
			term.add_new_lemma(lemma_id, language, notes)
			term.updated = True
			terms.setDirty(True)
			terms.joined_info.append({'lemma_id': lemma_id, 'term_id': term_id, 'language': language, 'notes': notes})
		else:
			original_notes = term.get_notes_of_lemma_id(lemma_id)
			terms.setDirty(True)
			if notes != original_notes:
				term.set_notes_of_lemma_id(notes, lemma_id)
				terms.add_edited_notes(term_id, lemma_id, notes)
		#TODO: save notes if notes changed
		self.setVisible(False)
		gui.application.getText().matchWithTerms()
		gui.application.getTextFrame().getTextPanel().update()
		gui.application.getTextFrame().setFocus(True)
		gui.application.getTextFrame().activateWindow()


class MultiLineTextField():
	def __init__(self, text, maxChar, lines, width, frame):
		self.textArea = customEdit(frame)
		self.setHeight(lines)
		self.textArea.setLineWrapColumnOrWidth(width)

		self.textAreaScrollPane = QtGui.QScrollArea()

		self.textAreaScrollPane.setWidgetResizable(False)
		self.container = QtGui.QWidget()
		layout = QtGui.QGridLayout(self.container)
		layout.addWidget(self.textArea)

		self.textAreaScrollPane.setWidget(self.container)
		self.textAreaScrollPane.setWidgetResizable(True)
		#self.textAreaScrollPane.setWidget(self.textArea)
		self.textAreaScrollPane.adjustSize()
		self.textAreaScrollPane.resize(self.textArea.size())

	def getTextAreaScrollPane(self):
		return self.textArea

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
		self.setAcceptRichText(False)

	def focusOutEvent(self, e):
		QtGui.QTextEdit.focusOutEvent(self,e)
		if(self.event):
			self.parent.lemma_was_changed()

	def focus_next_window(self, event):
		event.widget.tk_focusNext().focus()
		return ("break")

class StackedWidget(QtGui.QStackedWidget):
	def __init__(self):
		QtGui.QStackedWidget.__init__(self)

	def sizeHint(self):
		return self.currentWidget().size()
