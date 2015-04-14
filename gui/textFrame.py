import gui.utilities as utilities
import app.constants as constants
import gui.preferences as preferences
import gui.application
from app.TermStatus import TermStatus as TermStatus
import app.TermStatus
from PyQt4 import QtGui, QtCore
from gui.termFrame import TermFrame
import app.text as text

class TextFrame(QtGui.QMainWindow):
	def __init__(self):
		super(TextFrame, self).__init__()
		self.setWindowTitle(constants.SHORT_NAME)
		self.mainPanel = QtGui.QFrame()

		mainLayout = QtGui.QVBoxLayout()
		#mainLayout.setContentsMargins(5)
		self.mainPanel.setLayout(mainLayout)
		#self.mainPanel.setStyleSheet("border:5px; ")
		bar1 = QtGui.QHBoxLayout()
		self.tp = TextPanel(QtCore.QSize(preferences.getCurrWidthTextPanel(), preferences.getCurrHeightTextPanel()), self)
		self.tp.setGeometry(QtCore.QRect(20, 40, 601, 501))
		bar1.addWidget(self.getTextPanelScrollPane())
		mainLayout.addLayout(bar1)

		bar2 = QtGui.QHBoxLayout()
		self.labinfo = QtGui.QLabel('HI<html>&nbsp;\n&nbsp;</html>')
		self.labinfo.setTextFormat(QtCore.Qt.RichText)
		self.labinfo.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding , QtGui.QSizePolicy.MinimumExpanding )
		self.labinfo.setWordWrap(True)
		bar2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
		bar2.addWidget(self.labinfo)
		#self.lang = gui.application.getLanguage()

		langName = gui.application.getLanguage().getLangName()
		if langName == 'Korean':
			self.naverButton = QtGui.QPushButton("Lookup All on Naver")
			import functools
			self.naverButton.clicked.connect(functools.partial(self.lookupButtonClicked, langName))
			bar2.addWidget(self.naverButton)
		mainLayout.addLayout(bar2)


		self.setCentralWidget(self.mainPanel)
		self.crammerDock = None


		#self.setFixedSize(self.width(), self.height())
		self.resize(self.sizeHint())
		self.inSetData = False
		self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)

		self.shiftPressed = False

	def lookupNaver(self):
		from app.koreanHelper import get_root, get_root_korean
		from app.terms import  RootWord, Term
		terms = gui.application.getTerms()
		text = gui.application.getText()
		count = 0
		maxcount = 30000

		for textItem in text.getTextItems():
			print(textItem)
			skip = False
			foundRoot = False
			s = textItem.textItemValue
			if(s.replace(constants.PARAGRAPH_MARKER, "").strip() != ''):
				if not s in terms.termsDict:
					print(s)
					if count > maxcount: break
					count += 1
					root = get_root(s)
					if(root):
						rootWord = root[0][0]
						rootTrans = root[1]
					else:
						rootWord = None
						rootTrans = None
					if rootWord and rootWord in terms.rootDict:
						rootTerm = terms.rootDict[rootWord]
						foundRoot = True
					if foundRoot:
						print('found root skipping')
						newTerm = Term(s, terms.nextID(), rootTerm, rootTerm.id, True, False)
						terms.addTerm(newTerm)
						textItem.setLink(newTerm)
						terms.setDirty(True)
					else:
						kor_root = get_root_korean(s)
						if not root and kor_root:
							rootWord = kor_root[0]
						elif not root and not kor_root:
							print("OOPS")
							skip = True
						if not skip:
							if kor_root:
								rootDef = kor_root[1]
								if rootWord not in terms.rootDict:
									reLookupRoot = get_root(rootDef)
									if reLookupRoot != None:
										rootTrans = reLookupRoot[1]
										newID = len(terms.rootDict)+1
										#(self, id, word, definition, translation, priorSentence, sentenceCLOZE, sentence, followingSentence, source, status, new = True, updated = False):
										#1 for all new roots
										rootTerm = RootWord(newID, rootWord, rootDef, rootTrans, 'prior sentence TODO', 'sentenceCLOZETODO', 'SENTENCETODO', 'followingsentenceTODO', 'sourceTODO', 1, new=True, updated=False)
										terms.rootDict[rootWord] = rootTerm
								else:
									print('should never get here lolz')
									rootTerm = terms.rootDict[rootWord]
								newTerm = Term(s, terms.nextID(), rootTerm, rootTerm.id, True, False)
								terms.addTerm(newTerm)
								textItem.setLink(newTerm)
								terms.setDirty(True)
							else:
								rootDef = None



	def lookupButtonClicked(self, lang):
		lookup = {'Korean': self.lookupNaver}
		lookup[lang]()

	def getTextPanelScrollPane(self):
		return self.tp.getScrollPane()

	def setTitle(self, title):
		self.setWindowTitle(title)

	def getLabinfo(self):
		return self.labinfo

	def getTextPanel(self):
		return self.tp



	def closeEvent(self, e):
		import os
		terms = gui.application.getTerms()
		f = terms.getExportFile()
		exportOK = terms.isExportTermsToFileOK()
		if not exportOK:
			if f:
				if os.path.exists(f) and os.path.isfile(f):
					os.remove(f)
		else:
			exportOK = os.path.exists(f) and os.path.isfile(f)
		if terms.isDirty():
			if utilities.showYesNoQuestion("Your Vocabulary\n%s\nhas changed.\n\nSave to disk?" %os.path.abspath(terms.getFile()), True):
				backupFilename = os.path.abspath(terms.getFile())
				backupFilename = backupFilename[:len(backupFilename)-constants.TEXT_FILE_EXTENSION_LENGTH]+ ".bak"
				if not utilities.renameFile(terms.getFile(), backupFilename):
					utilities.showErrorMessage("Renaming your Vocabulary for Backup has failed.\n\nSorry, saving your vocabulary seems not be possible.")
				else:
					if not terms.isSaveTermsToDBOK():
						utilities.showErrorMessage("Writing your Vocabulary to\n"
										+ os.path.abspath(terms.getFile())
										+ "\nhas failed.\n\nSorry, saving your vocabulary seems not be possible.")
					else:
						if not exportOK:
							utilities.showInfoMessage("Success!\n\nYour Vocabulary has been successfully written to\n"
											+ os.path.abspath(terms.getFile())
											+ "\n\nThe previous version is available in\n"
											+ backupFilename)
						else:
							utilities.showInfoMessage("Success!\n\nYour Vocabulary has been successfully written to\n"
											+ os.path.abspath(terms.getFile())
											+ "\n\nThe previous version is available in\n"
											+ backupFilename
											+ "\n\nThe Vocabulary has been also exported to\n"
											+ os.path.abspath(f))
		termFrame = gui.application.getTermFrame()
		if termFrame:
			termFrame.setVisible(False)
			termFrame.close()
			gui.application.setTermFrame(None)
		self.setVisible(False)
		self.close()
		gui.application.setTextFrame(None)

		terms = None
		gui.application.setTerms(terms)

		text = gui.application.getText()
		text = None
		gui.application.setText(text)

		gui.application.getStartFrame().setVisible(True)

	def setChildrenFocusPolicy (self, policy):
		def recursiveSetChildFocusPolicy (parentQWidget):
			for childQWidget in parentQWidget.findChildren(QtGui.QWidget):
				childQWidget.setFocusPolicy(policy)
				recursiveSetChildFocusPolicy(childQWidget)
		recursiveSetChildFocusPolicy(self)


	def keyPressEvent(self, e):
		if e.isAutoRepeat() and e.key() == QtCore.Qt.Key_Shift:
			return
		text = gui.application.getText()
		marked = text.isRangeMarked()
		numPadDict = {QtCore.Qt.Key_5: TermStatus.Known,
		              QtCore.Qt.Key_4: TermStatus.Learning4,
		              QtCore.Qt.Key_3: TermStatus.Learning3,
		              QtCore.Qt.Key_2: TermStatus.Learning2,
		              QtCore.Qt.Key_1: TermStatus.Unknown,
		              QtCore.Qt.Key_I: TermStatus.Ignored,
		              QtCore.Qt.Key_0: TermStatus.Ignored,
		              QtCore.Qt.Key_6: TermStatus.WellKnown,
		              QtCore.Qt.Key_W: TermStatus.WellKnown}
		if (e.key() == QtCore.Qt.Key_Shift):
			self.shiftPressed = True
		elif (e.key() == QtCore.Qt.Key_Right):
			indexStart = min(text.getMarkIndexStart(),
				text.getMarkIndexEnd())
			indexEnd = max(text.getMarkIndexStart(),
				text.getMarkIndexEnd())
			if marked and indexEnd < len(text.getTextItems())-1:
				indexEnd += 1
				while text.getTextItemValueFromStartToEnd(indexEnd, indexEnd).strip() in [constants.PARAGRAPH_MARKER, '']:
					indexEnd += 1
				if not self.shiftPressed:
					indexStart = indexEnd
			elif not marked:
				indexStart = 0
				indexEnd = 0
				marked = True
				text.setRangeMarked(True)
			text.setMarkIndexStart(indexStart)
			text.setMarkIndexEnd(indexEnd)
			self.getTextPanel().checkScrollPane()
			self.getTextPanel().update()
			self.updateLabel(marked, indexStart, indexEnd)
		elif (e.key() == QtCore.Qt.Key_Down):
			indexStart = min(text.getMarkIndexStart(),
				text.getMarkIndexEnd())
			indexEnd = max(text.getMarkIndexStart(),
				text.getMarkIndexEnd())
			if marked and indexEnd < len(text.getTextItems())-1:
				curMarkPoint = text.getMarkedTextPoint()
				textLayout = QtGui.QTextLayout('X', self.tp.font())

				textLayout.beginLayout()
				line = textLayout.createLine()
				textLayout.endLayout()

				#1.8 not 1.3 because i dont know how to do the new paragraph things LOL
				fontHeight = 1.8 * (line.ascent() + line.descent() + line.leading() + 6)


				newPoint = QtCore.QPoint(curMarkPoint.x(), curMarkPoint.y()+fontHeight)
				nextLineTextItem =  text.getPointedTextItem(newPoint)
				if nextLineTextItem:
					indexEnd = text.getTextItemIndex(nextLineTextItem)
					while text.getTextItemValueFromStartToEnd(indexEnd, indexEnd).strip() in [constants.PARAGRAPH_MARKER, '']:
						indexEnd += 1
					if not self.shiftPressed:
						indexStart = indexEnd
			elif not marked:
				indexStart = 0
				indexEnd = 0
				marked = True
				text.setRangeMarked(True)
			text.setMarkIndexStart(indexStart)
			text.setMarkIndexEnd(indexEnd)
			self.getTextPanel().checkScrollPane()
			self.getTextPanel().update()
			self.updateLabel(marked, indexStart, indexEnd)
		elif(e.key() == QtCore.Qt.Key_Left):
			indexStart = min(text.getMarkIndexStart(),
				text.getMarkIndexEnd())
			indexEnd = max(text.getMarkIndexStart(),
				text.getMarkIndexEnd())
			if marked and indexStart > 0:
				indexStart -= 1
				while text.getTextItemValueFromStartToEnd(indexStart, indexStart).strip() in [constants.PARAGRAPH_MARKER, '']:
					indexStart -= 1
				if not self.shiftPressed:
					indexEnd = indexStart
			elif not marked:
				indexStart = len(text.getTextItems())
				indexEnd = len(text.getTextItems())
				marked = True
				text.setRangeMarked(True)
			text.setMarkIndexStart(indexStart)
			text.setMarkIndexEnd(indexEnd)
			self.getTextPanel().checkScrollPane()
			self.getTextPanel().update()
			self.updateLabel(marked, indexStart, indexEnd)
		elif(e.key() == QtCore.Qt.Key_Up):
			indexStart = min(text.getMarkIndexStart(),
				text.getMarkIndexEnd())
			indexEnd = max(text.getMarkIndexStart(),
				text.getMarkIndexEnd())
			if marked and indexStart > 0:
				curMarkPoint = text.getMarkedTextPoint()
				textLayout = QtGui.QTextLayout('X', self.tp.font())

				textLayout.beginLayout()
				line = textLayout.createLine()
				textLayout.endLayout()

				#black magic ahead
				fontHeight = 1 * (line.ascent() + line.descent() + line.leading() + 6)

				newPoint = QtCore.QPoint(curMarkPoint.x(), curMarkPoint.y()-fontHeight)
				#print(newPoint)
				nextLineTextItem =  text.getPointedTextItem(newPoint)
				if nextLineTextItem and newPoint.y() > 0:
					indexStart = text.getTextItemIndex(nextLineTextItem)
				while text.getTextItemValueFromStartToEnd(indexStart, indexStart).strip() in [constants.PARAGRAPH_MARKER, '']:
					indexStart -= 1
				if not self.shiftPressed:
					indexEnd = indexStart
			elif not marked:
				indexStart = len(text.getTextItems())-1
				indexEnd = len(text.getTextItems())-1
				marked = True
				text.setRangeMarked(True)
			text.setMarkIndexStart(indexStart)
			text.setMarkIndexEnd(indexEnd)
			self.getTextPanel().checkScrollPane()
			self.getTextPanel().update()
			self.updateLabel(marked, indexStart, indexEnd)
		elif(e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return):
			if marked:
				self.getTextPanel().startTermFrame()
		elif e.key() == QtCore.Qt.Key_Plus:
			if marked:
				term = text.getMarkedTermLink()
				if term:
					if not self.crammerDock:
						from gui.crammerFrame import CrammerFrame as CrammerFrame
						self.crammerDock = CrammerFrame([], True, self)
						#self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.crammerDock)

						self.crammerDock.move(self.pos().x()+self.frameGeometry().width(),self.pos().y())
						self.raise_()
						self.crammerDock.lower()
						self.crammerDock.setVisible(True)
						self.crammerDock.setWindowTitle("To Crammer")
					self.crammerDock.addTerm(term.root)
		elif e.key() == QtCore.Qt.Key_Minus:
			if marked:
				term = text.getMarkedTermLink()
				if term:
					if self.crammerDock:
						self.crammerDock.removeTerm(term.root)
						if self.crammerDock.noTerms():
							self.resetCrammerDock()
		elif(e.key() in numPadDict):
			if marked:
				term = text.getMarkedTermLink()
				if term:
					term.setStatus(numPadDict[e.key()])
					term.updated = True
					term.root.updated = True
					self.getTextPanel().update()
					gui.application.getTerms().setDirty(True)

	def resetCrammerDock(self):
		self.crammerDock.close()
		self.crammerDock = None
		#self.layout().activate()
		#self.resize(self.sizeHint())

	def keyReleaseEvent(self, e):
		if e.key() == QtCore.Qt.Key_Shift:
			print("released shift")
			self.shiftPressed = False

	def updateLabel(self, marked, startIndex, endIndex):
		text = gui.application.getText()
		textItems = text.getTextItems()

		if marked:
			term = text.getMarkedTermLink()
			if term:
				self.getLabinfo().setText(
							"<html><div style=\"text-align:%s;width:%s;\">%s</div></html>"
							%("right" if gui.application.getLanguage().getRightToLeft() else "left",
									preferences.getCurrWidthTextPanel(), term.displayWithStatusHTML()))
			else:
				s = text.getTextItemValueFromStartToEnd(startIndex, endIndex).strip()
				if s != "" and s != constants.PARAGRAPH_MARKER:
					self.getLabinfo().setText(
							"<html><div style=\"text-align:%s;width:%s;\">%s<br>(New Word)</div></html>"
							%("right" if gui.application.getLanguage().getRightToLeft() else "left",
									preferences.getCurrWidthTextPanel(), utilities.escapeHTML(s)))
			self.resize(self.sizeHint())



class TextPanel(QtGui.QWidget):
	def __init__(self, size, frame):
		super(TextPanel, self).__init__()
		#red orange yellow
		self.painters = [QtGui.QPainter(), QtGui.QPainter(), QtGui.QPainter()]
		self.painterDict = {'bad': self.painters[0], 'meh': self.painters[1], 'good': self.painters[2]}
		self.colorDict = {'bad':QtGui.QBrush(QtCore.Qt.red), 'meh': QtGui.QBrush(QtCore.Qt.yellow), 'good': QtGui.QBrush(QtCore.Qt.green)}
		self.frame = frame
		self.setAutoFillBackground(True)
		self.scrollArea = QtGui.QScrollArea()
		self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scrollArea.setMinimumSize(size)
		self.scrollArea.setMaximumSize(size)
		self.setMouseTracking(True)
		self.dragging = False
		self.mousePressed = False

		p = self.scrollArea.palette()
		p.setColor(self.scrollArea.backgroundRole(), QtCore.Qt.white)
		self.scrollArea.setPalette(p)
		self.scrollArea.setWidgetResizable(False)

		self.setGeometry(3000, 200, 1400, 300)

		#red orange yellow
		self.painters = [QtGui.QPainter(), QtGui.QPainter(), QtGui.QPainter()]
		self.painterDict = {'bad': self.painters[0], 'meh': self.painters[1], 'good': self.painters[2]}
		self.colorDict = {'bad':QtGui.QBrush(QtCore.Qt.red), 'meh': QtGui.QBrush(QtCore.Qt.yellow), 'good': QtGui.QBrush(QtCore.Qt.green)}
		self.scrollArea.setWidget(self)

	def checkScrollPane(self):
		text = gui.application.getText()
		indexEnd = max(text.getMarkIndexStart(),
				text.getMarkIndexEnd())
		position = text.getMarkedTextPoint()
		if position:
			self.scrollArea.ensureVisible(position.x(), position.y())


	def contextMenuEvent(self, e):
		def createAndAddNonActiveMenuItem(menu, text):
			action = QtGui.QAction("･･･ %s ･･･" %text, menu)
			action.setEnabled(False)
			menu.addAction(action)

		text = gui.application.getText()
		p1 = e.pos()
		item = text.getPointedTextItem(p1)
		if item:
			menu = QtGui.QMenu(self)
			linkedWord = item.getLink()
			if(linkedWord):
				editAction = menu.addAction("Edit [%s]" %item.getTextItemValue())
			else:
				editAction = menu.addAction("Create [%s]" %item.getTextItemValue())
			menu.addSeparator()
			createAndAddNonActiveMenuItem(menu, "Lookup Dictionary")
			lang = gui.application.getLanguage()
			dictArr = {}
			for i in range(3):
				if(lang.isURLset(i)):
					host = lang.getURLHost(i)
					if host:
						host = ' (%s)' %host
						tempAction = menu.addAction(host)
						dictArr[tempAction] = i
			menu.addSeparator()
			createAndAddNonActiveMenuItem(menu, "Set Status")
			actionArr = {}
			deleteAction = -1
			addToCrammerAction = -1
			removeFromCrammerAction = -1
			if linkedWord:
				for status in TermStatus.getAllActive():
					tempAction = menu.addAction(status.getStatusText())
					actionArr[tempAction] = status
				menu.addSeparator()
				deleteAction = menu.addAction("Delete Term")
				menu.addSeparator()
				addToCrammerAction = menu.addAction("Add to Crammer")
				removeFromCrammerAction = menu.addAction("Remove From Crammer")
			action = menu.exec_(self.mapToGlobal(e.pos()))
			terms = gui.application.getTerms()
			termFrame = gui.application.getTermFrame()
			if not termFrame:
				termFrame = TermFrame()
				gui.application.setTermFrame(termFrame)
			if action in actionArr:
				for a in actionArr:
					if action == a:
						item.setStatus(actionArr[a])
						item.updated = True
						linkedWord.root.updated = True
						terms.setDirty(True)
						self.update()
						break
			elif action in dictArr:
				gui.application.getLanguage().lookupWordInBrowser(item.getTextItemValue(),dictArr[action], True)
			elif action == editAction:
				if linkedWord:
					termFrame.startEdit(item.getLink(), '')
				else:
					s = item.getTextItemValue()
					index = text.getTextItems().index(item)
					text.setMarkIndexStart(index)
					text.setMarkIndexEnd(index)
					text.setRangeMarked(True)
					termFrame.startNew(s, text.getMarkedTextSentence(s))
			elif action == deleteAction:
				terms.deleteTerm(linkedWord)
				gui.application.getText().matchWithTerms()
				self.update()
			elif action == addToCrammerAction:
				if not self.frame.crammerDock:
					from gui.crammerFrame import CrammerFrame as CrammerFrame
					self.frame.crammerDock = CrammerFrame([], True, self.frame)
					#self.frame.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.frame.crammerDock)
					self.frame.crammerDock.setWindowTitle("To Crammer")
					self.frame.crammerDock.move(self.frame.pos().x()+self.frame.frameGeometry().width(),self.frame.pos().y())
					self.frame.raise_()
					self.frame.crammerDock.lower()
					self.frame.crammerDock.setVisible(True)
				self.frame.crammerDock.addTerm(linkedWord.root)
			elif action == removeFromCrammerAction:
				if self.frame.crammerDock:
					self.frame.crammerDock.removeTerm(linkedWord.root)
					if self.frame.crammerDock.noTerms():
						self.frame.resetCrammerDock()
						#self.frame.layout().activate()
						#self.frame.resize(self.frame.sizeHint())



	def isPopupTriggerHandled(self, e):
		r = False
		'''
		if e.isPopupTrigger()):
			TextPanelPopupMenu popupMenu = frame.getPopupMenu();
			Text text = Application.getText();
			Point p1 = e.getPoint();
			Point p2 = ((JViewport) e.getSource()).getViewPosition();
			Point p3 = new Point(p1.x + p2.x, p1.y + p2.y);
			int index = text.getPointedTextItemIndex(p3);
			TextItem ti = null;
			String w2 = "";
			String w3 = "";
			if (index >= 0) {
				ti = text.getTextItems().get(index);
				if ((index + 1) < text.getTextItems().size()) {
					w2 = ti.getTextItemValue()
							+ ti.getAfterItemValue()
							+ text.getTextItems().get(index + 1)
									.getTextItemValue();
					if ((index + 2) < text.getTextItems().size()) {
						w3 = w2
								+ text.getTextItems().get(index + 1)
										.getAfterItemValue()
								+ text.getTextItems().get(index + 2)
										.getTextItemValue();
					}
				}
			}
			popupMenu.updateMenu(ti, w2, w3);
			popupMenu.show((Component) e.getSource(), e.getX() + 10,
					e.getY() + 10);
			r = True
		else:
			r = False
			'''
		return r

	def mouseMoveEvent(self, e):
		text = gui.application.getText()
		p1 = e.pos()
		#print(p1)

		#p2 = ((JViewport) e.getSource()).getViewPosition()
		#p3 = QtCore.QPointF(p1.x() + p2.x(), p1.y() + p2.y())
		index = text.getPointedTextItemIndex(p1)
		if index >= 0:
			textItems = text.getTextItems()
			if self.mousePressed:
				startIndex = text.getMarkIndexStart()
				endIndex = index
				if startIndex < endIndex:
					text.setMarkIndexEnd(endIndex)
				self.dragging = True
				#endIndex = text.getMarkIndexEnd()

			t = textItems[index].getLink()
			if not t:
				s = textItems[index].getTextItemValue().strip()
				if s != "":
					self.frame.getLabinfo().setText(
							"<html><div style=\"text-align:%s;width:%s;\">%s<br>(New Word)</div></html>"
							%("right" if gui.application.getLanguage().getRightToLeft() else "left",
									preferences.getCurrWidthTextPanel(), utilities.escapeHTML(s)))
					#apparently orientation unneeded
					## utilities.setComponentOrientation(self.frame.getLabinfo())
					#utilities.setHorizontalAlignment(self.frame.getLabinfo())
			else:
				self.frame.getLabinfo().setText(
								"<html><div style=\"text-align:%s;width:%s;\">%s</div></html>"
								%("right" if gui.application.getLanguage().getRightToLeft() else "left",
										preferences.getCurrWidthTextPanel(), t.displayWithStatusHTML()))
				#utilities.setComponentOrientation(self.frame.getLabinfo())
				#utilities.setHorizontalAlignment(self.frame.getLabinfo())
			self.frame.resize(self.frame.sizeHint())
		#need to implement drag oops


	def mousePressEvent(self, e):
		if self.isPopupTriggerHandled(e):
			return
		if (e.button() == QtCore.Qt.LeftButton):
			text = gui.application.getText()
			p1 = e.pos()
			startIndex = text.getPointedTextItemIndex(p1)
			endIndex = startIndex
			text.setRangeMarked(startIndex >= 0)
			text.setMarkIndexStart(startIndex)
			text.setMarkIndexEnd(endIndex)
			self.update()
			self.dragging = False
			self.mousePressed = True

	def mouseReleaseEvent(self, e):
		self.mousePressed = False
		if self.isPopupTriggerHandled(e):
			return
		if (e.button() == QtCore.Qt.LeftButton):
			text = gui.application.getText()
			p1 = e.pos()
			endIndex = text.getPointedTextItemIndex(p1)
			if not text.isRangeMarked() and endIndex >= 0:
				text.setRangeMarked(True)
			if endIndex >= 0:
				text.setMarkIndexEnd(endIndex)

			self.update()
			#self.getTextPanel().requestFocus()
			self.startTermFrame()

	def startTermFrame(self):
		text = gui.application.getText()

		s = text.getMarkedText(self.dragging).replace(constants.PARAGRAPH_MARKER, "")
		if s != "":
			t = gui.application.getTerms().getTermFromKey(s.lower())
			termFrame = gui.application.getTermFrame()
			if not termFrame:
				termFrame = TermFrame()
				gui.application.setTermFrame(termFrame)
			if not t:
				termFrame.startNew(s, text.getMarkedTextSentence(s))
			else:
				termFrame.startEdit(t, text.getMarkedTextSentence(s))
			lang = gui.application.getLanguage()
			lang.lookupWordInBrowser(s, 3, False)
			lang.lookupWordInBrowser(s, 2, False)
			lang.lookupWordInBrowser(s, 1, False)


	def paintEvent(self, event):
		self.setFont(QtGui.QFont('Decorative', 20))
		text = gui.application.getText()
		lang = gui.application.getLanguage()
		langName = lang.getLangName()
		rtl = lang.getRightToLeft()
		fileName = gui.application.getText().getFile()
		textTitle = fileName[:len(fileName)-constants.TEXT_FILE_EXTENSION_LENGTH]
		gui.application.getTextFrame().setTitle('%s - [NEW: %d] - %s - %s' %(constants.SHORT_NAME,text.getUnlearnedWordCount(),langName, textTitle))
		marked = text.isRangeMarked()
		indexStart = min(text.getMarkIndexStart(),
				text.getMarkIndexEnd())
		indexEnd = max(text.getMarkIndexStart(),
				text.getMarkIndexEnd())
		g2d = QtGui.QPainter()
		g2d.begin(self)
		width = self.width() - (15 if rtl else 20)
		g2d.setRenderHint(QtGui.QPainter.Antialiasing, True)
		g2d.setRenderHint(QtGui.QPainter.TextAntialiasing, True)
		textLayout = QtGui.QTextLayout('X', self.font())
		font = self.font()
		fm = QtGui.QFontMetrics(font)
		textLayout.beginLayout()
		line = textLayout.createLine()
		textLayout.endLayout()

		h = line.ascent() + line.descent()  +2

		asc = line.ascent()
		if text.isCoordSet():
			viewPos = self.pos()
			top = -viewPos.y() - (h * 2)
			bot = -viewPos.y() + self.scrollArea.height() +(h * 2)
			for id, item in enumerate(text.getTextItems()):
				p = item.getTextItemPosition()
				d = item.getTextItemDimension()
				if p:
					if p.y() > top and p.y() < bot:
						term = item.getLink()
						notLastWord = not item.isLastWord()
						if not term:
							c = TermStatus.Null.getStatusColor()
						else:
							c = term.getStatus().getStatusColor()
						g2d.setBrush(c)
						if (notLastWord):
							g2d.fillRect(QtCore.QRectF(p, d), c)
						else:
							if rtl:
								g2d.fillRect(QtCore.QRectF(QtCore.QPointF(p.x() + 1, p.y()), QtCore.QSizeF(max(d.width() - 1,0), d.height())), c)
							else:
								#print('%s and the p is %s and the d is %s' %(item,p, d))
								g2d.fillRect(QtCore.QRectF(p, QtCore.QSizeF(max(d.width()-1,0), d.height())), c)
						if notLastWord:
							p2 = item.getAfterItemPosition()
							d2 = item.getAfterItemDimension()
							g2d.fillRect(QtCore.QRectF(p2, d2), c)
						#g2d.setBrush(QtCore.Qt.black)
						if marked and id >= indexStart and id <= indexEnd:
							rect = QtCore.QRectF(p.x(), p.y(), max(d.width() - 1,0), d.height())
							if rect.width() > 0:
								defaultPen = g2d.pen()
								pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
								g2d.setPen(pen)
								g2d.drawRect(rect)
								g2d.setPen(defaultPen)
						s = item.getTextItemValue()
						if s:
							textLayout = QtGui.QTextLayout("\u200F%s" %(s) if rtl else s, self.font())
							textLayout.beginLayout()
							line = textLayout.createLine()
							line.setPosition(QtCore.QPointF(0, 0))
							textLayout.endLayout()
							textLayout.draw(g2d, QtCore.QPointF(p.x(), p.y()))
						s = item.getAfterItemValue()
						if s:
							p = item.getAfterItemPosition()
							textLayout = QtGui.QTextLayout("\u200F%s" %(s) if rtl else s, self.font())
							textLayout.beginLayout()
							line = textLayout.createLine()
							line.setPosition(QtCore.QPointF(0, 0))
							textLayout.endLayout()
							textLayout.draw(g2d, QtCore.QPointF(p.x(), p.y()))
		else:
			x = 10
			y = 6
			lines = 1
			for item in text.getTextItems():
				#print(item)
				if item.getTextItemValue() == constants.PARAGRAPH_MARKER and item.getAfterItemValue() == "":
					x = 10
					y += 1.3 * (line.ascent() + line.descent() + line.leading() + 6)
					lines += 1
				else:
					t = "\u200F%s%s" if rtl else "%s%s" %(item.getTextItemValue(), item.getAfterItemValue())
					textLayout = QtGui.QTextLayout(t, self.font())
					textLayout.beginLayout()
					line = textLayout.createLine()
					line.setPosition(QtCore.QPointF(0, 0))
					textLayout.endLayout()
					if x + line.horizontalAdvance() > width:
						x = 10
						y += line.ascent() + line.descent() + line.leading() + 6
						lines += 1

					l = 0
					if item.getTextItemValue():
						tempLay = QtGui.QTextLayout("\u200F%s" if rtl else "%s" %(item.getTextItemValue()), self.font())
						tempLay.beginLayout()
						tempLine = tempLay.createLine()
						tempLine.setPosition(QtCore.QPointF(0, 0))
						tempLay.endLayout()
						l = tempLine.horizontalAdvance()
					l2 = 0

					if item.getAfterItemValue():

						tempLay = QtGui.QTextLayout("\u200F%s" if rtl else "%s" %(item.getAfterItemValue()), self.font())
						tempLay.beginLayout()
						tempLine = tempLay.createLine()
						tempLine.setPosition(QtCore.QPointF(0, 0))
						tempLay.endLayout()
						l2 = tempLine.horizontalAdvance()

					item.setTextItemDimension(QtCore.QSizeF(l, h))
					item.setAfterItemDimension(QtCore.QSizeF(l2, h))

					if rtl:
						item.setTextItemPosition(QtCore.QPointF(width - (x + l), y))
						item.setAfterItemPosition(QtCore.QPointF(width -(x + l + l2), y))
					else:
						item.setTextItemPosition(QtCore.QPointF(x, y))
						item.setAfterItemPosition(QtCore.QPointF(x + l, y))
					x += line.horizontalAdvance()
					#print(x)
			y += line.ascent() + line.descent() + line.leading() + 6
			self.resize(self.width() - 20, y)
			self.scrollArea.verticalScrollBar().setSingleStep(y/lines)
			self.setMinimumSize(self.size())
			self.setMaximumSize(self.size())
			text.setCoordSet(True)

	def getScrollPane(self):
		return self.scrollArea

