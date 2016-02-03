class LanguageDefinition:
	def __init__(self, name, isoCode, ttsAvailable, biggerFont, wordCharRegExp, makeCharacterWord, removeSpaces, rightToLeft):
		self.name = name
		self.isoCode = isoCode
		self.ttsAvailable = ttsAvailable
		self.biggerFont = biggerFont
		self.wordCharRegExp = wordCharRegExp
		self.makeCharacterWord = makeCharacterWord
		self.removeSpaces = removeSpaces
		self.rightToLeft = rightToLeft

	def getIsoCode(self):
		return self.isoCode

	def getName(self):
		return self.name

	def getWordCharRegExp(self):
		return self.wordCharRegExp

	def isBiggerFont(self):
		return self.biggerFont

	def isMakeCharacterWord(self):
		return self.makeCharacterWord

	def isRemoveSpaces(self):
		return self.removeSpaces

	def isRightToLeft(self):
		return self.rightToLeft

	def isTtsAvailable(self):
		return self.ttsAvailable
	