import gui.utilities as utilities
import app.constants as constants
import gui.preferences as preferences
import gui.application
from PyQt4 import QtGui, QtCore

class Text():
	def __init__(self, directory = None, text = None):
		self.markIndexEnd = 5
		self.markIndexStart = 5
		self.rangeMarked = False
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
				#self.textItems.append(TextItem("", s))
				print(start)
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
		terms = gui.application.getTerms()
		for i in range(len(self.textItems)):
			i = terms.match(self, i)

	def isCoordSet(self):
		return self.coordSet

	def setCoordSet(self, bool):
		self.coordSet = bool

	def getFile(self):
		return self.file

	def getUnlearnedWordCount(self):
		return 56

	def isRangeMarked(self):
		return self.rangeMarked

	def getMarkIndexEnd(self):
		return self.markIndexEnd

	def getMarkIndexStart(self):
		return self.markIndexStart

	def getPointedTextItemIndex(self, p):
		for id, t in enumerate(self.textItems):
			if t.isPointOnTextItem(p):
				return id
		return -1

	def getPointedTextItem(self, p):
		for id, t in enumerate(self.textItems):
			if t.isPointOnTextItem(p):
				return t
		return None

	def getTextItems(self):
		return self.textItems

	def setRangeMarked(self, bool):
		self.rangeMarked = bool

	def setMarkIndexStart(self, markIndexStart):
		self.markIndexStart = markIndexStart

	def setMarkIndexEnd(self, markIndexEnd):
		self.markIndexEnd = markIndexEnd

	def getMarkedTextPoint(self):
		if self.rangeMarked:
			indexEnd = max(self.markIndexStart, self.markIndexEnd)
			if indexEnd >= 0:
				ti = self.textItems[indexEnd]
				return ti.getTextItemPosition()
		return None

	def getMarkedTerm(self):
		if self.rangeMarked:
			indexEnd = max(self.markIndexStart, self.markIndexEnd)
			if indexEnd >= 0:
				ti = self.textItems[indexEnd]
				return ti
		return None

	def getMarkedText(self, dragging):
		s = ""
		if self.rangeMarked:
			indexStart = min(self.markIndexStart, self.markIndexEnd)
			indexEnd = max(self.markIndexStart, self.markIndexEnd)
			if indexStart >= 0 and indexEnd >= 0:
				if indexStart == indexEnd and not dragging:
					ti = self.textItems[indexStart]
					term = ti.getLink()
					if not term:
						s = ti.getTextItemValue()
					else:
						s = term.getTerm()
				else:
					s = ''.join([x.getTextItemValue()+x.getAfterItemValue() for x in self.textItems[indexStart:indexEnd]])
					s += self.textItems[indexEnd].getTextItemValue()
		return s

	def getMarkedTextSentence(self, term):
		s = ''
		if self.rangeMarked:
			indexStart = min(self.markIndexStart, self.markIndexEnd) - 9
			indexEnd = max(self.markIndexStart, self.markIndexEnd) + 9
			indexStart = max(0, indexStart)
			indexEnd = min(len(self.textItems) - 1, indexEnd)
			s = '%s%s%s' %('' if indexStart == 0 else '… ',
			               self.getTextRange(indexStart, indexEnd, True),
			               "" if indexEnd == len(self.textItems) - 1 else " …")
			s = s.replace(term, "{" + term + "}")
		else:
			s = "???"
		return s.replace(constants.PARAGRAPH_MARKER, "")

	def getTextRange(self, f, to, lastAlso):
		r = ""
		i = max(f, 0)
		while i < len(self.textItems) and i <= to:
			ti = self.textItems[i]
			r += ti.getTextItemValue()
			if i < to or lastAlso:
				r += ti.getAfterItemValue()
			i += 1
		return r

class TextItem():
	def __init__(self, textItemValue, afterItemValue, status = 'bad'):
		self.textItemValue = textItemValue
		self.afterItemValue = afterItemValue
		self.textItemLowerCaseValue = textItemValue.lower()
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
			if (p.x() > self.textItemPosition.x()):
				if (p.y() > self.textItemPosition.y()):
					if (p.x() < (self.textItemPosition.x() + self.textItemDimension.width())):
						if (p.y() < (self.textItemPosition.y() + self.textItemDimension.height())):
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


