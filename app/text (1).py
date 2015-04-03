import gui.utilities as utilities
import app.constants as constants
import gui.preferences as preferences
import gui.application
from PyQt4 import QtGui, QtCore

class Text():
	def __init__(self, directory = None, text = None):
		self.markIndexEnd = 5
		self.markIndexStart = 5
		if(directory):
			self.file = directory
			self.text = utilities.readFileIntoString(directory)
			self.textItems = []
			self.splitText()
			self.coordSet = False
		else:
			self.file = None
			self.text = text
			self.textItems = []
			self.splitText()
			self.coordSet = False

	def splitText(self):
		import re
		text = self.text.replace(constants.EOL, " %s " %constants.PARAGRAPH_MARKER)
		text = text.replace(constants.UNIX_EOL, " %s " %constants.PARAGRAPH_MARKER)
		text = text.replace(constants.TAB, " ")
		text = text.strip()
		if (gui.application.getLanguage().getMakeCharacterWord()):
			#no idea what this does
			pass
		text = text.replace("\\s{2,", " ")
		substitutions = gui.application.getLanguage().getCharSubstitutions().split("\\|")
		for subst in substitutions:
			if "=" in subst:
				fromto = (subst + "=x").split("=")
				if len(fromto) == 3:
					text = text.replace(fromto[0].strip(), fromto[1].strip())
		text = text.strip()
		lang = gui.application.getLanguage()
		pattern = re.compile(r'[^%s%s]+' %(constants.PARAGRAPH_MARKER, lang.getWordCharRegExp()))

		start = 0
		noSpaces = lang.getRemoveSpaces()
		match = pattern.finditer(text)
		for m in match:
			s = text[m.start():m.end()]
			if (noSpaces):
				s = s.replaceAll("\\s", "")
			if (start == m.start()):
				self.textItems.append(TextItem("", s))
				start = m.end()
			else:
				pref = text[start:m.start()]
				if (pref == constants.PARAGRAPH_MARKER):
					self.textItems.append(TextItem(pref, ""))
					#print('added pref')
					s = utilities.leftTrim(s)
					if s != "":
						#print('appe')
						self.textItems.append(TextItem("", s))
				else:
					#print('els %s' %text[start:m.start()])
					self.textItems.append(TextItem(
							text[start:m.start()], s))
				start = m.end()
		s = text[start:]
		if s:
			self.textItems.append(TextItem(s, ""))

	def matchWithTerms(self):
		pass

	def isCoordSet(self):
		return self.coordSet

	def setCoordSet(self, bool):
		self.coordSet = bool

	def getFile(self):
		return self.file

	def getUnlearnedWordCount(self):
		return 56

	def isRangeMarked(self):
		return False

	def getMarkIndexEnd(self):
		return self.markIndexEnd

	def getMarkIndexStart(self):
		return self.markIndexStart

class TextItem():
	def __init__(self, textItemValue, afterItemValue, status = 'bad'):
		self.textItemValue = textItemValue
		self.afterItemValue = afterItemValue
		self.status = status
		self.term = None
		self.textItemPosition = None
		self.textItemDimension = None
		self.afterItemDimension = None
		self.afterItemPosition = None
		self.lastWord = True

	def getAfterItemDimension(self):
		return self.afterItemDimension

	def getAfterItemPosition(self):
		return self.afterItemPosition

	def getAfterItemValue(self):
		return self.afterItemValue

	def getLink(self):
		return self.term

	def getTextItemDimension(self):
		return self.textItemDimension

	def getTextItemLowerCaseValue(self):
		return self.textItemLowerCaseValue

	def getTextItemPosition(self):
		return self.textItemPosition

	def getTextItemValue(self):
		return self.textItemValue

	def isLastWord(self):
		return self.lastWord

	def isPointOnTextItem(self, p):
		if self.textItemPosition and self.textItemDimension:
			if (p.x > self.textItemPosition.x):
				if (p.y > self.textItemPosition.y):
					if (p.x < (self.textItemPosition.x + self.textItemDimension.width + self.afterItemDimension.width)):
						if (p.y < (self.textItemPosition.y + self.textItemDimension.height)):
							return True
		return False

	def setAfterItemDimension(self, afterItemDimension):
		self.afterItemDimension = afterItemDimension

	def setAfterItemPosition(self, afterItemPosition):
		self.afterItemPosition = afterItemPosition

	def setLastWord(self, lastWord):
		self.lastWord = lastWord
	
	def setLink(self, term):
		self.term = term

	def setTextItemDimension(self, textItemDimension):
		self.textItemDimension = textItemDimension

	def setTextItemPosition(self, textItemPosition):
		self.textItemPosition = textItemPosition

	def __str__(self):
		return "[%s / %s]" %(self.textItemValue, self.afterItemValue)

	def getStatus(self):
		return self.term.getStatus()

	def setStatus(self, status):
		self.term.setStatus(status)


