import os
import app.constants as constants
import gui.utilities as utilities

FILE_IDENTIFIER = "FLTRLANGPREFS"
KEY_char_substitutions = "charSubstitutions"
default_char_substitutions = "´='|`='|’='|‘='|′='|‵='"

KEY_dictionary_url_1 = "dictionaryURL1"
default_dictionary_url_1 = "http://translate.google.com/?ie=UTF-8&sl=auto&tl=en&text=###"

KEY_dictionary_url_2 = "dictionaryURL2"
default_dictionary_url_2 = "http://endic.naver.com/search.nhn?sLn=en&isOnlyViewEE=N&query=###"

KEY_dictionary_url_3 = "dictionaryURL3"
default_dictionary_url_3 = ""

KEY_open_automatically_url_1 = "openAutomaticallyURL1"
default_open_automatically_url_1 = "0"

KEY_open_automatically_url_2 = "openAutomaticallyURL2"
default_open_automatically_url_2 = "0"

KEY_open_automatically_url_3 = "openAutomaticallyURL3"
default_open_automatically_url_3 = "0"

KEY_font_name = "fontName"
default_font_name = "Dialog"

KEY_font_size = "fontSize"
default_font_size = "20"

KEY_status_font_name = "statusFontName"
default_status_font_name = "Dialog"

KEY_status_font_size = "statusFontSize"
default_status_font_size = "15"

KEY_word_char_regex = "wordCharRegExp"
default_word_char_regex = "\u4E00-\u9FFF\uF900-\uFAFF\u1100-\u11FF\u3130-\u318F\uAC00-\uD7A0"

KEY_word_encoding_url_1 = "wordEncodingURL1"
default_word_encoding_url_1 = constants.ENCODING

KEY_word_encoding_url_2 = "wordEncodingURL2"
default_word_encoding_url_2 = constants.ENCODING

KEY_word_encoding_url_3 = "wordEncodingURL3"
default_word_encoding_url_3 = constants.ENCODING

KEY_make_character_word = "makeCharacterWord"
default_make_character_word = "0"

KEY_remove_spaces = "removeSpaces"
default_remove_spaces = "0"

KEY_right_to_left = "rightToLeft"
default_right_to_left = "0"

KEY_export_template = "exportTemplate"
default_export_template = "$w\\t$t\\t$s\\t$r\\t$a\\t$k"

KEY_export_statuses = "exportStatuses"
default_export_statuses = "1|2|3|4"

KEY_do_export = "doExport"
default_do_export = "1"

class Language:
	def __init__(self, pref_file):
		super(Language, self).__init__()
		self.langFile = pref_file
		self.textDir = os.path.join(os.path.dirname(self.langFile), '%s%s'%(self.getLangName(), constants.TEXT_DIR_SUFFIX))

		import configparser
		config = configparser.ConfigParser()
		config.read(pref_file, encoding = constants.ENCODING)
		self.lang_prefs = config
		self.saveFile()

	def get_bool_pref(self, key, def_):
		return self.getIntPref(key, def_) != 0

	def get_char_substitutions(self):
		return self.getPref(KEY_char_substitutions,
		                    default_char_substitutions)

	def get_dictionary_url_1(self):
		return self.getPref(KEY_dictionary_url_1, default_dictionary_url_1)

	def get_dictionary_url_2(self):
		return self.getPref(KEY_dictionary_url_2, default_dictionary_url_2)

	def get_dictionary_url_3(self):
		return self.getPref(KEY_dictionary_url_3, default_dictionary_url_3)
	
	#TODO: finish refactoring the names of functions to meet standards....
	def getDoExport(self):
		return self.get_bool_pref(KEY_do_export, default_do_export)
	

	def getExportStatuses(self):
		return self.getPref(KEY_export_statuses, default_export_statuses)
	

	def getExportTemplate(self):
		return self.getPref(KEY_export_template, default_export_template)
	

	def getFontName(self):
		return self.getPref(KEY_font_name, default_font_name)
	

	def getFontSize(self):
		return self.getIntPref(KEY_font_size, default_font_size)
	

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
		return self.get_bool_pref(KEY_make_character_word,
		                          default_make_character_word)
	

	def getOpenAutomaticallyURL1(self):
		return self.get_bool_pref(KEY_open_automatically_url_1,
		                          default_open_automatically_url_1)
	

	def getOpenAutomaticallyURL2(self):
		return self.get_bool_pref(KEY_open_automatically_url_2,
		                          default_open_automatically_url_2)
	

	def getOpenAutomaticallyURL3(self):
		return self.get_bool_pref(KEY_open_automatically_url_3,
		                          default_open_automatically_url_3)
	

	def getPref(self, key, def_):
		if (key in self.langFile):
			value = self.langFile[key].strip()
		else:
			value = def_.strip()
		return value

	def getRemoveSpaces(self):
		return self.get_bool_pref(KEY_remove_spaces, default_remove_spaces)
	

	def getRightToLeft(self):
		return self.get_bool_pref(KEY_right_to_left, default_right_to_left)
	

	def getStatusFontName(self):
		return self.getPref(KEY_status_font_name, default_status_font_name)
	

	def getStatusFontSize(self):
		return self.getIntPref(KEY_status_font_size,
		                       default_status_font_size)
	

	def getTextDir(self):
		return self.textDir
	

	def getURLHost(self, linkNo):
		if (not self.isURLset(linkNo)):
			return ""
		u = ""
		if (linkNo == 1):
			u = self.get_dictionary_url_1()
		elif (linkNo == 2):
			u = self.get_dictionary_url_2()
		elif (linkNo == 3):
			u = self.get_dictionary_url_3()
		try:
			from urllib.parse import urlparse
			url = urlparse(u)
			return url.hostname
		except ValueError:
			return ""

	def getWordCharRegExp(self):
		return self.getPref(KEY_word_char_regex, default_word_char_regex)
	

	def getWordEncodingURL1(self):
		return self.getPref(KEY_word_encoding_url_1,
		                    default_word_encoding_url_1)
	

	def getWordEncodingURL2(self):
		return self.getPref(KEY_word_encoding_url_2,
		                    default_word_encoding_url_2)
	

	def getWordEncodingURL3(self):
		return self.getPref(KEY_word_encoding_url_3,
		                    default_word_encoding_url_3)
	

	def isURLset(self, linkNo):
		URL = ""
		if (linkNo == 1):
			URL = self.get_dictionary_url_1()
		elif (linkNo == 2):
			URL = self.get_dictionary_url_2()
		elif (linkNo == 3):
			URL = self.get_dictionary_url_3()
		return URL.startswith(constants.URL_BEGIN)
	

	def lookupWordInBrowser(self, word, linkNo, always):
		if (not self.isURLset(linkNo)):
			return
		URL = ""
		encoding = ""
		autoOpen = False
		if (linkNo == 1):
			URL = self.get_dictionary_url_1()
			encoding = self.getWordEncodingURL1()
			autoOpen = self.getOpenAutomaticallyURL1()
		elif (linkNo == 2):
			URL = self.get_dictionary_url_2()
			encoding = self.getWordEncodingURL2()
			autoOpen = self.getOpenAutomaticallyURL2()
		elif (linkNo == 3):
			URL = self.get_dictionary_url_3()
			encoding = self.getWordEncodingURL3()
			autoOpen = self.getOpenAutomaticallyURL3()
		if (always or autoOpen):
			import urllib.parse
			utilities.openURLInDefaultBrowser(URL.replace(
					constants.TERM_PLACEHOLDER,
					urllib.parse.quote(word.strip())))


	def putPref(self, key, value):
		if(FILE_IDENTIFIER not in self.lang_prefs):
			self.lang_prefs[FILE_IDENTIFIER] = {}
		self.lang_prefs[FILE_IDENTIFIER][key] = str(value).strip()


	def saveFile(self):
		import configparser
		config = configparser.ConfigParser()
		config[FILE_IDENTIFIER] = {KEY_char_substitutions: self.get_char_substitutions(),
		                           KEY_word_char_regex: self.getWordCharRegExp(),
		                           KEY_make_character_word: 1 if self.getMakeCharacterWord() else 0,
		                           KEY_remove_spaces: 1 if self.getRemoveSpaces() else 0,
		                           KEY_right_to_left: 1 if self.getRightToLeft() else 0,
		                           KEY_font_name: self.getFontName(),
		                           KEY_font_size: self.getFontSize(),
		                           KEY_status_font_name: self.getStatusFontName(),
		                           KEY_status_font_size: self.getStatusFontSize(),
		                           KEY_dictionary_url_1: self.get_dictionary_url_1(),
		                           KEY_word_encoding_url_1: self.getWordEncodingURL1(),
		                           KEY_open_automatically_url_1: self.getOpenAutomaticallyURL1(),
		                           KEY_dictionary_url_2: self.get_dictionary_url_2(),
		                           KEY_word_encoding_url_2: self.getWordEncodingURL2(),
		                           KEY_open_automatically_url_2: self.getOpenAutomaticallyURL2(),
		                           KEY_dictionary_url_3: self.get_dictionary_url_3(),
		                           KEY_word_encoding_url_3: self.getWordEncodingURL3(),
		                           KEY_open_automatically_url_3:  1 if self.getOpenAutomaticallyURL3() else 0,
		                           KEY_export_template: self.getExportTemplate(),
		                           KEY_export_statuses: self.getExportStatuses(),
		                           KEY_do_export:  1 if self.getDoExport() else 0}
		fileName = self.langFile
		with open(fileName, 'w', encoding = constants.ENCODING) as configfile:
			config.write(configfile)