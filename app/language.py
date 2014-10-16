import os
import app.constants as constants
import gui.utilities as utilities

FILE_IDENTIFIER = "FLTRLANGPREFS"
KEYcharSubstitutions = "charSubstitutions"
DFTcharSubstitutions = "´='|`='|’='|‘='|′='|‵='"

KEYdictionaryURL1 = "dictionaryURL1"
DFTdictionaryURL1 = "http://translate.google.com/?ie=UTF-8&sl=auto&tl=en&text=###"

KEYdictionaryURL2 = "dictionaryURL2"
DFTdictionaryURL2 = "http://endic.naver.com/search.nhn?sLn=en&isOnlyViewEE=N&query=###"

KEYdictionaryURL3 = "dictionaryURL3"
DFTdictionaryURL3 = ""

KEYopenAutomaticallyURL1 = "openAutomaticallyURL1"
DFTopenAutomaticallyURL1 = "0"

KEYopenAutomaticallyURL2 = "openAutomaticallyURL2"
DFTopenAutomaticallyURL2 = "0"

KEYopenAutomaticallyURL3 = "openAutomaticallyURL3"
DFTopenAutomaticallyURL3 = "0"

KEYfontName = "fontName"
DFTfontName = "Dialog"

KEYfontSize = "fontSize"
DFTfontSize = "20"

KEYstatusFontName = "statusFontName"
DFTstatusFontName = "Dialog"

KEYstatusFontSize = "statusFontSize"
DFTstatusFontSize = "15"

KEYwordCharRegExp = "wordCharRegExp"
DFTwordCharRegExp = "\u4E00-\u9FFF\uF900-\uFAFF\u1100-\u11FF\u3130-\u318F\uAC00-\uD7A0"

KEYwordEncodingURL1 = "wordEncodingURL1"
DFTwordEncodingURL1 = constants.ENCODING

KEYwordEncodingURL2 = "wordEncodingURL2"
DFTwordEncodingURL2 = constants.ENCODING

KEYwordEncodingURL3 = "wordEncodingURL3"
DFTwordEncodingURL3 = constants.ENCODING

KEYmakeCharacterWord = "makeCharacterWord"
DFTmakeCharacterWord = "0"

KEYremoveSpaces = "removeSpaces"
DFTremoveSpaces = "0"

KEYrightToLeft = "rightToLeft"
DFTrightToLeft = "0"

KEYexportTemplate = "exportTemplate"
DFTexportTemplate = "$w\\t$t\\t$s\\t$r\\t$a\\t$k"

KEYexportStatuses = "exportStatuses"
DFTexportStatuses = "1|2|3|4"

KEYdoExport = "doExport"
DFTdoExport = "1"
class Language():
	def __init__(self, prefFile):
		super(Language, self).__init__()
		self.langFile = prefFile
		self.textDir = os.path.join(os.path.dirname(self.langFile), '%s%s'%(self.getLangName(), constants.TEXT_DIR_SUFFIX))

		import configparser
		config = configparser.ConfigParser()
		config.read(prefFile, encoding = constants.ENCODING)
		self.langPrefs = config
		self.saveFile()

	def getBoolPref(self, key, def_):
		return self.getIntPref(key, def_) != 0

	def getCharSubstitutions(self):
		return self.getPref(KEYcharSubstitutions,
				DFTcharSubstitutions)

	def getDictionaryURL1(self):
		return self.getPref(KEYdictionaryURL1, DFTdictionaryURL1)

	def getDictionaryURL2(self):
		return self.getPref(KEYdictionaryURL2, DFTdictionaryURL2)

	def getDictionaryURL3(self):
		return self.getPref(KEYdictionaryURL3, DFTdictionaryURL3)
	

	def getDoExport(self):
		return self.getBoolPref(KEYdoExport, DFTdoExport)
	

	def getExportStatuses(self):
		return self.getPref(KEYexportStatuses, DFTexportStatuses)
	

	def getExportTemplate(self):
		return self.getPref(KEYexportTemplate, DFTexportTemplate)
	

	def getFontName(self):
		return self.getPref(KEYfontName, DFTfontName)
	

	def getFontSize(self):
		return self.getIntPref(KEYfontSize, DFTfontSize)
	

	def getIntPref(self, key, def_):
		try:
			result = int(self.getPref(key, def_))
		except ValueError:
			result = int(def_)
		return result
	

	def getLangFile(self):
		return self.langFile
	

	def getLangName(self):
		head, tail = os.path.split(self.langFile)
		return tail[:(len(tail) - constants.LANG_SETTINGS_FILE_SUFFIX_LENGTH)]

	def getMakeCharacterWord(self):
		return self.getBoolPref(KEYmakeCharacterWord,
				DFTmakeCharacterWord)
	

	def getOpenAutomaticallyURL1(self):
		return self.getBoolPref(KEYopenAutomaticallyURL1,
				DFTopenAutomaticallyURL1)
	

	def getOpenAutomaticallyURL2(self):
		return self.getBoolPref(KEYopenAutomaticallyURL2,
				DFTopenAutomaticallyURL2)
	

	def getOpenAutomaticallyURL3(self):
		return self.getBoolPref(KEYopenAutomaticallyURL3,
				DFTopenAutomaticallyURL3)
	

	def getPref(self, key, def_):
		if (key in self.langFile):
			value = self.langFile[key].strip()
		else:
			value = def_.strip()
		return value

	def getRemoveSpaces(self):
		return self.getBoolPref(KEYremoveSpaces, DFTremoveSpaces)
	

	def getRightToLeft(self):
		return self.getBoolPref(KEYrightToLeft, DFTrightToLeft)
	

	def getStatusFontName(self):
		return self.getPref(KEYstatusFontName, DFTstatusFontName)
	

	def getStatusFontSize(self):
		return self.getIntPref(KEYstatusFontSize,
				DFTstatusFontSize)
	

	def getTextDir(self):
		return self.textDir
	

	def getURLHost(self, linkNo):
		if (not self.isURLset(linkNo)):
			return ""
		u = ""
		if (linkNo == 1):
			u = self.getDictionaryURL1()
		elif (linkNo == 2):
			u = self.getDictionaryURL2()
		elif (linkNo == 3):
			u = self.getDictionaryURL3()
		try:
			from urllib.parse import urlparse
			url = urlparse(u)
			return url.hostname
		except ValueError:
			return ""

	def getWordCharRegExp(self):
		return self.getPref(KEYwordCharRegExp, DFTwordCharRegExp)
	

	def getWordEncodingURL1(self):
		return self.getPref(KEYwordEncodingURL1,
				DFTwordEncodingURL1)
	

	def getWordEncodingURL2(self):
		return self.getPref(KEYwordEncodingURL2,
				DFTwordEncodingURL2)
	

	def getWordEncodingURL3(self):
		return self.getPref(KEYwordEncodingURL3,
				DFTwordEncodingURL3)
	

	def isURLset(self, linkNo):
		URL = ""
		if (linkNo == 1):
			URL = self.getDictionaryURL1()
		elif (linkNo == 2):
			URL = self.getDictionaryURL2()
		elif (linkNo == 3):
			URL = self.getDictionaryURL3()
		return URL.startswith(constants.URL_BEGIN)
	

	def lookupWordInBrowser(self, word, linkNo, always):
		if (not self.isURLset(linkNo)):
			return
		URL = ""
		encoding = ""
		autoOpen = False
		if (linkNo == 1):
			URL = self.getDictionaryURL1()
			encoding = self.getWordEncodingURL1()
			autoOpen = self.getOpenAutomaticallyURL1()
		elif (linkNo == 2):
			URL = self.getDictionaryURL2()
			encoding = self.getWordEncodingURL2()
			autoOpen = self.getOpenAutomaticallyURL2()
		elif (linkNo == 3):
			URL = self.getDictionaryURL3()
			encoding = self.getWordEncodingURL3()
			autoOpen = self.getOpenAutomaticallyURL3()
		if (always or autoOpen):
			import urllib.parse
			utilities.openURLInDefaultBrowser(URL.replace(
					constants.TERM_PLACEHOLDER,
					urllib.parse.quote(word.strip())))


	def putPref(self, key, value):
		if(FILE_IDENTIFIER not in self.langPrefs):
			self.langPrefs[FILE_IDENTIFIER] = {}
		self.langPrefs[FILE_IDENTIFIER][key] = str(value).strip()


	def saveFile(self):
		import configparser
		config = configparser.ConfigParser()
		config[FILE_IDENTIFIER] = {KEYcharSubstitutions: self.getCharSubstitutions(),
		                           KEYwordCharRegExp: self.getWordCharRegExp(),
		                           KEYmakeCharacterWord: 1 if self.getMakeCharacterWord() else 0,
		                           KEYremoveSpaces: 1 if self.getRemoveSpaces() else 0,
		                           KEYrightToLeft: 1 if self.getRightToLeft() else 0,
		                           KEYfontName: self.getFontName(),
		                           KEYfontSize: self.getFontSize(),
		                           KEYstatusFontName: self.getStatusFontName(),
		                           KEYstatusFontSize: self.getStatusFontSize(),
		                           KEYdictionaryURL1: self.getDictionaryURL1(),
		                           KEYwordEncodingURL1: self.getWordEncodingURL1(),
		                           KEYopenAutomaticallyURL1: self.getOpenAutomaticallyURL1(),
		                           KEYdictionaryURL2: self.getDictionaryURL2(),
		                           KEYwordEncodingURL2: self.getWordEncodingURL2(),
		                           KEYopenAutomaticallyURL2: self.getOpenAutomaticallyURL2(),
		                           KEYdictionaryURL3: self.getDictionaryURL3(),
		                           KEYwordEncodingURL3: self.getWordEncodingURL3(),
		                           KEYopenAutomaticallyURL3:  1 if self.getOpenAutomaticallyURL3() else 0,
		                           KEYexportTemplate: self.getExportTemplate(),
		                           KEYexportStatuses: self.getExportStatuses(),
		                           KEYdoExport:  1 if self.getDoExport() else 0}
		fileName = self.langFile
		with open(fileName, 'w', encoding = constants.ENCODING) as configfile:
			config.write(configfile)