import sys, os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../app')))
from app.languageDef import LanguageDefinition
class LanguageDefinitions():
	def __init__(self):
		self.defArray = []
		self.defArray.append(LanguageDefinition("English", "en", True, False, "",
				False, False, False))
		self.nameHashMap = {}
		self.defArray.append(LanguageDefinition("Korean", "ko", True, True,
				"\\u4E00-\\u9FFF\\uF900-\\uFAFF\\u1100-\\u11FF"
						+ "\\u3130-\\u318F\\uAC00-\\uD7A0", False, False, False))
		for ld in self.defArray:
			self.nameHashMap[ld.getName()] = ld

	def getTextList(self):
		result = []
		for ld in self.defArray:
			result.append(ld.getName())
		return result

	def getArray(self):
		return self.defArray