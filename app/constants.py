import sys, os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../img')))

SHORT_VERSION = "0.8.6"
VERSION = "{0} (28-Aug-2012)".format(SHORT_VERSION)

SHORT_NAME = "FLTR"
LONG_NAME = "Foreign Language Text Reader"
WEBSITE = "http://fltr.googlecode.com"
COPYRIGHT = "Copyright © 2012 {0} Developers".format(SHORT_NAME)

ICON_PATH = os.path.normpath(os.path.join(here, '../img/icon128.png'))
LOCK_FILE_PATH = os.path.join(os.path.expanduser('~'), '.fltrlock')
PREF_FILE_PATH = os.path.join(os.path.expanduser('~'), '.fltrprefsPYTHON')

TEXT_DIR_SUFFIX = "_Texts"
TEXT_DIR_SUFFIX_LENGTH = len(TEXT_DIR_SUFFIX)

LANG_SETTINGS_FILE_SUFFIX = "_Settings.csv"
LANG_SETTINGS_FILE_SUFFIX_LENGTH = len(LANG_SETTINGS_FILE_SUFFIX)

DB = 'fltr.db'

WORDS_FILE_SUFFIX = "_Words.csv"
EXPORT_WORDS_FILE_SUFFIX = "_Export.txt"

TEXT_FILE_EXTENSION = ".txt"
TEXT_FILE_EXTENSION_LENGTH = len(TEXT_FILE_EXTENSION)

MAX_DATA_LENGTH_START_FRAME = 35
MAX_TEXT_LENGTH_START_FRAME = 30
MAX_LANG_LENGTH_START_FRAME = 30

PARAGRAPH_MARKER = u'¶'
ENCODING = "UTF-8-sig"

TAB = "\t"
EOL = "\r\n"
UNIX_EOL = "\n"
TERMS_SEPARATOR = " ･ "
URL_BEGIN = "http://"
TERM_PLACEHOLDER = "###"
