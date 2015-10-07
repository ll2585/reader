import gui.utilities as utilities
import app.constants as constants
import gui.preferences as preferences
import gui.application
from app.TermStatus import TermStatus as TermStatus
import app.TermStatus
from PyQt4 import QtGui, QtCore
from gui.termFrame import TermFrame
import app.text as text
import functools

class CrammerFrame(QtGui.QMainWindow):
	def __init__(self, terms, openedByText = False, frame = None):
		super(CrammerFrame, self).__init__()
		self.toCrammer = terms
		self.openedByText = openedByText
		self.frame = frame
		if self.openedByText:
			print("opened by frame")
			self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
			self.lower()
		self.initUI(self.toCrammer)

	def initUI(self, terms):

		self.setWindowTitle(constants.SHORT_NAME)
		self.terms = terms
		self.mainPanel = QtGui.QFrame()

		self.termModel = TermTableModel(self.terms)

		self.table_view = TableView(self)
		self.table_view.setModel(self.termModel)
		self.table_view.resizeColumnToContents(0)
		self.table_view.resizeColumnToContents(1)
		self.table_view.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Fixed)
		self.table_view.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Fixed)
		mainLayout = QtGui.QVBoxLayout()
		self.mainPanel.setLayout(mainLayout)
		bar1 = QtGui.QHBoxLayout()
		bar1.addWidget(self.table_view)
		mainLayout.addLayout(bar1)

		bar2 = QtGui.QHBoxLayout()
		self.exportButton = QtGui.QPushButton('Export to CSV', self)
		self.exportButton.clicked.connect(self.export)
		bar2.addWidget(self.exportButton)

		self.startButton = QtGui.QPushButton('Start', self)
		self.startButton.clicked.connect(self.startCrammer)
		bar2.addWidget(self.startButton)
		mainLayout.addLayout(bar2)
		self.setFixedSize(600,400)
		self.setCentralWidget(self.mainPanel)

	def addTerm(self, term):
		if term not in self.toCrammer:
			self.toCrammer.append(term)
			self.termModel.addTerm(term)

	def removeTerm(self, term):
		if term in self.toCrammer:
			self.toCrammer.remove(term)
			self.termModel.removeTerm(term)

	def noTerms(self):
		return len(self.toCrammer) == 0

	def getTerms(self):
		return self.toCrammer

	def startCrammer(self):
		from crammer.gui.gui import FlashCardWindow
		cards = self.termModel.getCardList()
		if len(cards) > 0:
			f = FlashCardWindow(preExistingCards = cards)
		else:
			print("PICK CARDS IDIOT")

	def closeEvent(self, e):
		if not self.openedByText:
			print("CLOSED")
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

			crammer = gui.application.getCrammerFrame()
			crammer = None
			gui.application.setCrammerFrame(crammer)

			gui.application.getStartFrame().setVisible(True)
		else:
			print("refocus frame")
			self.frame.setFocus()
			self.frame.resetCrammerDock()

	def closeMe(self):
		self.frame.resetCrammerDock()


	def export(self):
		import os, csv
		fileName = QtGui.QFileDialog.getSaveFileName(self,
                "Save CSV", '',
                "CSV (*.csv);;All Files (*)")

		if not fileName:
			return

		newpath = os.path.abspath(fileName)

		cards = self.termModel.getCardList()
		with open(newpath, 'w', newline='',  encoding='utf-8') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=',',
			                        quotechar='"', quoting=csv.QUOTE_ALL)
			for c in cards:
				csvwriter.writerow([c.front,c.back])
		done = QtGui.QMessageBox()
		done.setText("Done!")
		done.exec_()

class TableView(QtGui.QTableView):

	def __init__(self, parent):
		super(TableView, self).__init__()
		self.parent = parent
		self.setItemDelegateForColumn(0, ItemDelegate(self))
		self.setItemDelegateForColumn(6, ButtonDelegate(self))

	def cellButtonClicked(self, row):
		print(self.sender())
		rows = self.model().rowCount(self)
		print(self.currentIndex().row())
		allRows = rows
		rowsToRemove = -1
		for r in range(0,allRows):
			if self.sender() == self.indexWidget((self.model().index(r, 6))):
				print('wtf row %s' %r)
				rowsToRemove = r
				break
		if rowsToRemove != -1:
			print('removing row %s' %rowsToRemove)
			del self.model().mylist[rowsToRemove]
			self.model().beginRemoveRows(QtCore.QModelIndex(), rowsToRemove, rowsToRemove)
			self.model().removeRows(rowsToRemove, 1)
			self.model().endRemoveRows()
			if(len(self.model().mylist)==0):
				self.parent.closeMe()



class TermTableModel(QtCore.QAbstractTableModel):
	def __init__(self, terms):
		super(TermTableModel, self).__init__()
		self.header = ['✓', '#', 'Word', 'Definition', 'Status', 'Source','[X]']
		self.mylist = []
		for id, t in enumerate(terms):
			self.mylist.append([True, id, t.word, t.definition,t.status.getStatusText(), t.source,False])

	def rowCount(self, parent):
		return len(self.mylist)

	def columnCount(self, parent):
		return len(self.header)

	def headerData(self, col, orientation, role):
		if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
			return self.header[col]
		return None

	def data(self, index, role):
		#self.refreshMyList()
		if not index.isValid():
			return None
		elif role == QtCore.Qt.EditRole:
			return self.mylist[index.row()][index.column()]  # node.data method defined above (string)
		elif role == QtCore.Qt.CheckStateRole and index.column() == 0:
			if self.mylist[index.row()][0]:
				return QtCore.Qt.Checked
			else:
				return QtCore.Qt.Unchecked
		elif role != QtCore.Qt.DisplayRole:
			return None
		if index.column() == 0:
			return
		if index.column() == 1:
			return index.row() + 1
		return self.mylist[index.row()][index.column()]

	def getCardList(self):
		checkedItems = []
		from crammer.model.model import Card
		for t in self.mylist:
			if t[0]:
				word = t[2]
				defin = t[3]
				checkedItems.append(Card(word, defin))
		return checkedItems

	def setData(self, index, value, role=QtCore.Qt.DisplayRole):
		if (role == QtCore.Qt.CheckStateRole):
			self.mylist[index.row()][index.column()] = not self.mylist[index.row()][index.column()]
		elif role == QtCore.Qt.EditRole:
			#finish this later
			id = self.mylist[index.row()][1]
			self.mylist[index.row()][index.column()]=value
			self.dataChanged.emit(index, index)
			terms = gui.application.getTerms()

			#print('changing %s' %self.termIdDict[id])

		return True

	def flags(self, index):
		if(index.column() == 0):
			return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
		elif(index.column() in [2,3,4]):
			return QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
		else:
			return QtCore.Qt.ItemIsEnabled

	def removeTerm(self, term):
		rowsToRemove = -1
		for row, t in enumerate(self.mylist):
			print('%s - %s' %(t[2], term.word))
			if t[2] == term.word:
				print("OK")
				rowsToRemove = row
				del self.mylist[row]
				break
		if rowsToRemove != -1:
			self.beginRemoveRows(QtCore.QModelIndex(), rowsToRemove, rowsToRemove)
			self.removeRows(rowsToRemove, 1)
			self.endRemoveRows()

	def addTerm(self, term):
		t = term
		self.mylist.append([True, len(self.mylist), t.word, t.definition,t.status.getStatusText(), t.source,False])
		self.layoutChanged.emit()



class ItemDelegate(QtGui.QStyledItemDelegate):
	def __init__(self,parent):
		self.m_lastClickedIndex = None
		super(ItemDelegate, self).__init__(parent)

	def paint(self, painter, option, index):

		state = index.data(QtCore.Qt.CheckStateRole)
		opt = QtGui.QStyleOptionButton()
		opt.state = QtGui.QStyle.State_Enabled

		if state == QtCore.Qt.Unchecked:
			opt.state |= QtGui.QStyle.State_Off
		elif state == QtCore.Qt.PartiallyChecked:
			opt.state |= QtGui.QStyle.State_NoChange
		elif state == QtCore.Qt.Checked:
			opt.state |= QtGui.QStyle.State_On
		opt.rect = QtGui.QApplication.style().subElementRect(QtGui.QStyle.SE_CheckBoxIndicator, opt, None)
		x = option.rect.center().x() - opt.rect.width() / 2
		y = option.rect.center().y() - opt.rect.height() / 2
		opt.rect.moveTo(x,y)

		QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_CheckBox, opt, painter)
		'''
		old code just in case

		viewItemOption = QtGui.QStyleOptionViewItemV4(option)

		if index.column() == 0:
			textMargin = QtGui.QApplication.style().pixelMetric(QtGui.QStyle.PM_FocusFrameHMargin) + 1
			newRect = QtGui.QStyle.alignedRect(option.direction, QtCore.Qt.AlignCenter, QtCore.QSize(option.decorationSize.width() + 5, option.decorationSize.height()), QtCore.QRect(option.rect.x() + textMargin, option.rect.y(), option.rect.width() - (2*textMargin), option.rect.height()))
			viewItemOption.rect = newRect
		super(ItemDelegate, self).paint(painter, viewItemOption, index)
		'''

	def editorEvent(self, event, model, option, index):
		'''
		old code just in case
		flags = model.flags(index)
		if not (flags and QtCore.Qt.ItemIsUserCheckable) or not(flags and QtCore.Qt.ItemIsEnabled):
			return False
		value = index.data(QtCore.Qt.CheckStateRole)

		if event.type() == QtCore.QEvent.MouseButtonRelease:
			textMargin = QtGui.QApplication.style().pixelMetric(QtGui.QStyle.PM_FocusFrameHMargin) + 1
			checkRect = QtGui.QStyle.alignedRect(option.direction, QtCore.Qt.AlignCenter,  option.decorationSize,  QtCore.QRect(option.rect.x() + (2 * textMargin), option.rect.y(), option.rect.width() - ( 2 * textMargin), option.rect.height()))
			if not checkRect.contains(event.pos()):
				return False
		elif event.type() == QtCore.QEvent.KeyPress:
			if event.key() != QtCore.Qt.Key_Space and event.key() != QtCore.Qt.Key_Select:
				return False
		else:
			return False
		state = QtCore.Qt.Unchecked if value == QtCore.Qt.Checked else QtCore.Qt.Checked
		return model.setData(index, state, QtCore.Qt.CheckStateRole)
		'''
		if event.type() == QtCore.QEvent.MouseButtonPress:
			self.m_lastClickedIndex = index
		elif event.type() == QtCore.QEvent.MouseButtonRelease:
			if index != self.m_lastClickedIndex:
				pass
			else:
				e = event
				if e.button() != QtCore.Qt.LeftButton:
					pass
				else:
					self.m_lastClickedIndex = QtCore.QModelIndex()
					opt = QtGui.QStyleOptionButton()
					opt.rect = QtGui.QApplication.style().subElementRect(QtGui.QStyle.SE_CheckBoxIndicator, opt, None)
					x = option.rect.center().x() - opt.rect.width() / 2
					y = option.rect.center().y() - opt.rect.height() / 2
					opt.rect.moveTo(x,y)


					if opt.rect.contains(e.pos()):

						state = index.data(QtCore.Qt.CheckStateRole)
						if state == QtCore.Qt.Unchecked:
							state = QtCore.Qt.PartiallyChecked
						elif state == QtCore.Qt.PartiallyChecked:
							state = QtCore.Qt.Checked
						elif state == QtCore.Qt.Checked:
							state = QtCore.Qt.Unchecked
						model.setData(index,state, QtCore.Qt.CheckStateRole)
					return True
		return super(ItemDelegate, self).editorEvent(event, model, option, index)

class ButtonDelegate(QtGui.QStyledItemDelegate):
	def __init__(self, parent):
		super(ButtonDelegate, self).__init__(parent)

	def paint(self, painter, option, index):
		if not self.parent().indexWidget(index):
			self.parent().setIndexWidget(index, QtGui.QPushButton("Delete", self.parent(), clicked=functools.partial(self.parent().cellButtonClicked, index)))

	def editorEvent(self, event, model, option, index):
		return super(ButtonDelegate, self).editorEvent(event, model, option, index)

class CrammerDock(QtGui.QDockWidget):
	def __init__(self, parent):
		self.m_lastClickedIndex = None
		super(CrammerDock, self).__init__(parent)
		self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
		terms = gui.application.getTerms()
		unknownCards = terms.getUnknownCards()
		self.toCrammer = []
		self.parent = parent
		self.initUI(self.toCrammer)


	def addTerm(self, term):
		if term not in self.toCrammer:
			self.toCrammer.append(term)
			self.termModel.addTerm(term)

	def removeTerm(self, term):
		if term in self.toCrammer:
			self.toCrammer.remove(term)
			self.termModel.removeTerm(term)

	def noTerms(self):
		return len(self.toCrammer) == 0

	def getTerms(self):
		return self.toCrammer


	def initUI(self, terms):

		self.setWindowTitle(constants.SHORT_NAME)
		self.terms = terms
		self.mainPanel = QtGui.QFrame()

		self.termModel = TermTableModel(self.terms)

		self.table_view = TableView(self)
		self.table_view.setModel(self.termModel)
		self.table_view.resizeColumnToContents(0)
		self.table_view.resizeColumnToContents(1)
		self.table_view.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Fixed)
		self.table_view.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Fixed)
		mainLayout = QtGui.QVBoxLayout()
		self.mainPanel.setLayout(mainLayout)
		bar1 = QtGui.QHBoxLayout()
		bar1.addWidget(self.table_view)
		mainLayout.addLayout(bar1)

		bar2 = QtGui.QHBoxLayout()
		self.exportButton = QtGui.QPushButton('Export to CSV', self)
		self.exportButton.clicked.connect(self.export)
		self.startButton = QtGui.QPushButton('Start', self)
		self.startButton.clicked.connect(self.startCrammer)
		bar2.addWidget(self.exportButton)
		bar2.addWidget(self.startButton)
		mainLayout.addLayout(bar2)
		self.setFixedSize(600,400)
		self.setWidget(self.mainPanel)

	def startCrammer(self):
		from crammer.gui.gui import FlashCardWindow
		cards = self.termModel.getCardList()
		if len(cards) > 0:
			f = FlashCardWindow(preExistingCards = cards)
		else:
			print("PICK CARDS IDIOT")

	def export(self):
		cards = self.termModel.getCardList()
		print(cards)

	def closeMe(self):
		self.parent.resetCrammerDock()