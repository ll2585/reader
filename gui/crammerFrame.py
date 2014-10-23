import gui.utilities as utilities
import app.constants as constants
import gui.preferences as preferences
import gui.application
from app.TermStatus import TermStatus as TermStatus
import app.TermStatus
from PyQt4 import QtGui, QtCore
from gui.termFrame import TermFrame
import app.text as text

class CrammerFrame(QtGui.QMainWindow):
	def __init__(self, terms):
		super(CrammerFrame, self).__init__()
		self.setWindowTitle(constants.SHORT_NAME)
		self.terms = terms
		self.mainPanel = QtGui.QFrame()

		self.termModel = TermTableModel(self.terms)

		table_view = TableView()
		table_view.setModel(self.termModel)
		table_view.resizeColumnToContents(0)
		table_view.resizeColumnToContents(1)
		table_view.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Fixed)
		table_view.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Fixed)
		mainLayout = QtGui.QVBoxLayout()
		#mainLayout.setContentsMargins(5)
		self.mainPanel.setLayout(mainLayout)
		#self.mainPanel.setStyleSheet("border:5px; ")
		bar1 = QtGui.QHBoxLayout()
		bar1.addWidget(table_view)
		mainLayout.addLayout(bar1)

		bar2 = QtGui.QHBoxLayout()
		self.startButton = QtGui.QPushButton('Start', self)
		self.startButton.clicked.connect(self.startCrammer)
		bar2.addWidget(self.startButton)
		mainLayout.addLayout(bar2)
		self.setFixedSize(600,400)
		self.setCentralWidget(self.mainPanel)

	def startCrammer(self):
		from crammer.gui.gui import FlashCardWindow
		cards = self.termModel.getCardList()
		if len(cards) > 0:
			f = FlashCardWindow(preExistingCards = cards)
		else:
			print("PICK CARDS IDIOT")

class TableView(QtGui.QTableView):

	def __init__(self):
		super(TableView, self).__init__()
		self.setItemDelegateForColumn(0, ItemDelegate())

class TermTableModel(QtCore.QAbstractTableModel):
	def __init__(self, terms):
		super(TermTableModel, self).__init__()
		self.header = ['✓', '#', 'Word', 'Definition', 'Status', 'Source']
		self.terms = terms
		self.mylist = []
		self.checkedItems = []
		self.cardDict = {}
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
		from crammer.model.model import Card
		for id, t in enumerate(self.terms):
			self.cardDict[id+1] = Card(t.word, t.definition)
			self.mylist.append([False, id+1, t.word, t.definition,t.status.getStatusText(), t.source])

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
		return self.mylist[index.row()][index.column()]

	def getCardList(self):
		return self.checkedItems

	def setData(self, index, value, role=QtCore.Qt.DisplayRole):
		if (role == QtCore.Qt.CheckStateRole):
			self.mylist[index.row()][index.column()] = not self.mylist[index.row()][index.column()]
			card = self.cardDict[self.mylist[index.row()][1]]
			if self.mylist[index.row()][index.column()]:
				self.checkedItems.append(card)
			else:
				try:
					self.checkedItems.remove(card)
				except ValueError:
					pass
		row = index.row()
		self.mylist[index.row()][index.column()]=value
		self.dataChanged.emit(index, index)
		return True

	def flags(self, index):
		if(index.column() == 0):
			return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
		elif(index.column() in [2,3,4]):
			return QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
		else:
			return QtCore.Qt.ItemIsEnabled

class ItemDelegate(QtGui.QStyledItemDelegate):
	def __init__(self):
		self.m_lastClickedIndex = None
		super(ItemDelegate, self).__init__()

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

