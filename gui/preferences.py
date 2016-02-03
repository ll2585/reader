FILE_IDENTIFIER = "FLTRPREFSPython"
import app.constants as constants

instance = None

def getBoolPreference(key, def_):
	return (getIntPreference(key, (1 if def_ else 0) != 0))

def getCurrDialogFontSizePercent():
	return getIntPreference("currDialogFontSizePercent", 100)

def getCurrHeightTextPanel():
	return getIntPreference("currHeightTextPanel", 400)

def getCurrLang():
	return getPreference("currLang", "[None]")

def getCurrLookAndFeel():
	return getPreference("currLookAndFeel", "system")

def getCurrMainDir():
	return getPreference("currMainDir", "[Select…]")

def getCurrText():
	return getPreference("currText", "[None]")

def putCurrLang(s):
	putPreference("currLang", s)

def putCurrMainDir(s):
	putPreference("currMainDir", s)

def putCurrText(s):
	putPreference("currText", s)

def getCurrWidthTextPanel():
	return getIntPreference("currWidthTextPanel", 600)

def getIntPreference(key, def_):
	s = getPreference(key.strip(), str(def_).strip())
	try:
		result = int(s)
	except BaseException:
		result = def_
	return result


def putCurrWidthTextPanel(i):
	putIntPreference("currWidthTextPanel", i)

def getCurrPopupMenusNested():
	return getBoolPreference("currPopupMenusNested", False)

def putCurrVocabMaxResult(i):
	putIntPreference("currVocabMaxResults", i)

def putCurrVocabSortOrder(i):
	putIntPreference("currVocabSortOrder", i)


def putCurrVocabStatusFilter(s):
	putPreference("currVocabStatusFilter", s)


def putCurrVocabTextFilter(s):
	putPreference("currVocabTextFilter", s)


def putCurrVocabWordFilter(s):
	putPreference("currVocabWordFilter", s)


def putCurrXPosStartWindow(i):
	putIntPreference("currXPosStartWindow", i)


def putCurrXPosTermWindow(i):
	putIntPreference("currXPosTermWindow", i)


def putCurrXPosTextWindow(i):
	putIntPreference("currXPosTextWindow", i)


def putCurrYPosStartWindow(i):
	putIntPreference("currYPosStartWindow", i)

def putCurrHeightTextPanel(i):
	putIntPreference("currHeightTextPanel", i)


def putCurrYPosTermWindow(i):
	putIntPreference("currYPosTermWindow", i)


def putCurrYPosTextWindow(i):
	putIntPreference("currYPosTextWindow", i)

def putBoolPreference(key, value):
		putIntPreference(key, (1 if value else 0))


def putCurrDialogFontSizePercent(i):
	putIntPreference("currDialogFontSizePercent", i)

def putCurrLookAndFeel(s):
	putPreference("currLookAndFeel", s)

def putDBPath(s):
	putPreference("db", s)

def getDBPath():
	return getPreference("db", "fltr.db")

def putCurrPopupMenusNested(b):
	putBoolPreference("currPopupMenusNested", b)

def putIntPreference(key, value):
	putPreference(key.strip(), str(value).strip())

def getPreference(key, def_):
	global instance
	if (instance == None):
		instance = _Preferences()
	if(FILE_IDENTIFIER not in instance.prefs):
		instance.prefs[FILE_IDENTIFIER] = {}
	if (key in instance.prefs[FILE_IDENTIFIER]):
		value = instance.prefs[FILE_IDENTIFIER][key].strip()
	else:
		value = def_.strip()
	putPreference(key, value)
	return value

def putPreference(_key, _value):
	global instance
	if(instance == None):
		instance = _Preferences()
	if(FILE_IDENTIFIER not in instance.prefs):
		instance.prefs[FILE_IDENTIFIER] = {}
	instance.prefs[FILE_IDENTIFIER][_key.strip()] = _value.strip()
	instance.savePreferences()

class _Preferences():
	def __init__(self):
		super(_Preferences, self).__init__()
		fileName = constants.PREF_FILE_PATH
		import configparser
		config = configparser.ConfigParser()
		config.read(fileName, encoding = constants.ENCODING)
		self.prefs = config


	def savePreferences(self):
		fileName = constants.PREF_FILE_PATH
		with open(fileName, 'w', encoding = constants.ENCODING) as configfile:
			self.prefs.write(configfile)
'''


	public static getCurrDialogFontSizePercent():
		return getIntPreference("currDialogFontSizePercent", 100)


	public static getCurrHeightTextPanel():
		return getIntPreference("currHeightTextPanel", 400)




	public static getCurrLookAndFeel():
		return getPreference("currLookAndFeel", "system")





	public static getCurrVocabMaxResults():
		return getIntPreference("currVocabMaxResults", 0)


	public static getCurrVocabSortOrder():
		return getIntPreference("currVocabSortOrder", 1)


	public static getCurrVocabStatusFilter():
		return getPreference("currVocabStatusFilter", "1|2|3|4")


	public static getCurrVocabTextFilter():
		return getPreference("currVocabTextFilter", "[All Terms]")


	public static getCurrVocabWordFilter():
		return getPreference("currVocabWordFilter", "")




	public static getCurrXPosStartWindow(dft):
		return getIntPreference("currXPosStartWindow", dft)


	public static getCurrXPosTermWindow(dft):
		return getIntPreference("currXPosTermWindow", dft)


	public static getCurrXPosTextWindow(dft):
		return getIntPreference("currXPosTextWindow", dft)


	public static getCurrYPosStartWindow(dft):
		return getIntPreference("currYPosStartWindow", dft)


	public static getCurrYPosTermWindow(dft):
		return getIntPreference("currYPosTermWindow", dft)


	public static getCurrYPosTextWindow(dft):
		return getIntPreference("currYPosTextWindow", dft)


	private static getIntPreference(key, def):
		s = getPreference(key.trim(), Integer.toString(def)
				.trim())
		result
		try {
			result = Integer.parseInt(s)
	 catch (Exception e):
			result = def
	
		return result


	def putCurrText(s):
		putPreference("currText", s)


	

	def putPreference(key, value):
		if (instance == null):
			instance = new Preferences()
	
		instance.prefs.put(key.trim(), value.trim())
		instance.savePreferences()


	private Hashtable<String, String> prefs
	private fileName

	private static Preferences instance = null

	public static scaleIntValue(i):
		return (int) (((float) i * (float) Preferences
				.getCurrDialogFontSizePercent()) / 100.0f)



}
'''