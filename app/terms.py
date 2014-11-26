import os
import app.constants as constants
import gui.utilities as utilities
from app.text import Text as Text
from app.TermStatus import TermStatus as TermStatus
import gui.application
import sqlite3


def lastIndexOf(arr, item):
	for i in range(len(arr)-1, -1, -1):
		if item == arr[i]:
			return i
		else:
			raise ValueError("rindex(lis, item): item not in lis")


class Terms():
	def __init__(self):
		self.data = []
		self.keyIndex = {}
		self.keyIndex2 = {}
		self.exportFile = None
		self.file = None
		self.dirty = False
		self.db = ''
		self.dir = ''
		self.rootDict = {}
		self.termsDict = {}
		self.deletedIDs = []
		self.deletedRoots = []
		self.termsCount = {}

	def isLoadTermsFromFileOK(self, file):
		import os
		r = False
		self.file = file
		parent = os.path.dirname(file)
		lang = gui.application.getLanguage().getLangName()
		self.exportFile = os.path.join(parent, '%s%s' %(lang, constants.EXPORT_WORDS_FILE_SUFFIX))
		if(os.path.exists(file) and os.stat(file).st_size!=0):
			with open(file, 'r', encoding=constants.ENCODING) as f:
				lines = f.readlines()
			for line in lines:
				if(line != ''):
					cols = line.split(constants.TAB)
					cnt = len(cols)
					if cnt >= 1:
						if cnt >= 5:
							status = cols[4].strip()
							intStatus = 1
							if status:
								try:
									intStatus = int(status)
								except ValueError:
									intStatus = 1
							#(word, definition, translation, priorSentence, sentenceCLOZE, sentence, followingSentence, source, status):
							self.addTerm(Term(cols[0].strip(), RootWord(cols[0].strip(), cols[1].strip(),
									cols[2].strip(), '', '', cols[3].strip(), '', '', intStatus)))
						elif (cnt == 4):
							self.addTerm(Term(cols[0].strip(), RootWord(cols[0].strip(), cols[1].strip(),
									cols[2].strip(), '', '', cols[3].strip(), '', '', 1)))
						elif (cnt == 3):
							self.addTerm(Term(cols[0].strip(), RootWord(cols[0].strip(), cols[1].strip(),
									cols[2].strip(), '', '', '', '', '', 1)))
						elif (cnt == 2):
							self.addTerm(Term(cols[0].strip(), RootWord(cols[0].strip(), cols[1].strip(),
									'', '', '', '', '', '', 1)))
						else: #cnt == 1
							self.addTerm(Term(cols[0].strip(), RootWord(cols[0].strip(), '?',
									'', '', '', '', '', '', 1)))
				self.dirty = False
				r = True
		return r

	def isLoadTermsFromDBOK(self, dir, db):
		import os
		file = dir
		self.dir = dir
		self.db = db
		parent = os.path.dirname(file)
		lang = gui.application.getLanguage().getLangName()
		exportFile = os.path.join(parent, '%s%s' %(lang, constants.EXPORT_WORDS_FILE_SUFFIX))
		try:
			conn = sqlite3.connect(db)
			langs = (dir,)
			roots = conn.execute('SELECT * from terms WHERE language = ?', (lang,)).fetchall()
			words = conn.execute('SELECT * from word WHERE language = ?', (lang,)).fetchall()
			for w in roots:
				#(self, id, word, definition, translation, priorSentence, sentenceCLOZE, sentence, followingSentence, source, status, new = True, updated = False):
				newRoot = RootWord(w[0], w[2], w[3], w[4], w[5], w[6], w[7], w[8], w[9], w[10], new=False, updated = False)
				self.rootDict[w[2]] = newRoot
			for w in words:
				#(self, word, rootWord, rootID, new = True, updated = False):
				newTerm = Term(w[2], w[0], self.rootDict[w[3]], w[4], new=False, updated = False)
				self.addTerm(newTerm)
			#data.trimToSize()
			self.dirty = False
			r = True
		except BaseException as e:
			print(e)
			self.dirty = True
			r = False
		return r

	def getUnknownCards(self):
		unknownCards = []
		for t in self.rootDict:
			if self.rootDict[t].status not in [TermStatus.WellKnown, TermStatus.Ignored]:
				unknownCards.append(self.rootDict[t])
		return unknownCards

	def getTermFromKey(self, key):
		if key in self.keyIndex.keys():
			index = self.keyIndex[key]
			return self.getTermFromIndex(index)
		return None

	def getTermFromIndex(self, index):
		if index < 0 or index >= len(self.data):
			return None
		return self.data[index]

	def deleteTerm(self, t):
		key = t.getKey()
		if key in self.keyIndex:
			index = self.keyIndex[key]
			self.data[index] = None
			del self.keyIndex[key]
			l = t.getWordCount()
			firstWord = t.getText().getTextItems()[0].getTextItemValue().lower()
			#do multiwords later
			## self.keyIndex2[firstWord][l][index] = None
			self.dirty = True
			idTuple = (t.id,)
			print(idTuple)
			self.deletedIDs.append(idTuple)

	def deleteRoot(self, rootWord):
		if rootWord in self.rootDict:
			rootTerm = self.rootDict[rootWord]
			del self.rootDict[rootWord]
			self.dirty = True
			idTuple = (rootTerm.id,)
			self.deletedRoots.append(idTuple)

	def addTerm(self, t):
		if t.getKey() in self.keyIndex.keys():
			self.data[self.keyIndex[t.getKey()]] = t
		else:
			self.data.append(t)
			index = lastIndexOf(self.data,t)
			self.keyIndex[t.getKey()] = index
			l = t.getWordCount()
			firstWord = t.getText().getTextItems()[0].getTextItemValue().lower()
			temp = {}
			if firstWord not in self.keyIndex2.keys():
				self.keyIndex2[firstWord] = temp
			temp = self.keyIndex2[firstWord]
			if l not in temp:
				temp2 = []
				temp[l] = temp2
			temp2 = temp.get(l)
			temp2.append(index)
		if not t.word in self.termsDict:
			self.termsDict[t.word] = t
		self.dirty = True
		termRoot = t.root.word
		self.addCountToRoot(termRoot)

	def subtractCountFromRoot(self, rootWord):
		self.termsCount[rootWord] -= 1

	def getRootCount(self, rootWord):
		return self.termsCount[rootWord]

	def addCountToRoot(self, rootWord):
		if rootWord not in self.termsCount:
			self.termsCount[rootWord] = 1
		else:
			self.termsCount[rootWord] += 1

	def match(self, text, index):
		nextIndex = -1
		ti = text.getTextItems()[index]
		if ti.getTextItemLowerCaseValue() in self.keyIndex2:
			temp = self.keyIndex2.get(ti.getTextItemLowerCaseValue())
			for key, val in temp.items():
				value = val
				count = key
				for index2 in value:
					t = self.data[index2]
					text2 = text.getTextRange(index,
							(index + count) - 1, False)
					if t and t.getKey() == text2.lower():
						nextIndex = index + count
						for i in range(index, nextIndex):
							ti2 = text.getTextItems()[i]
							ti2.setLink(t)
							ti2.setLastWord(i == ((index + count) - 1))
						return nextIndex
			nextIndex = index + 1
			ti.setLink(None)
			ti.setLastWord(True)
		else:
			nextIndex = index + 1
			ti.setLink(None)
			ti.setLastWord(True)
		return nextIndex

	def setDirty(self, dirty):
		self.dirty = dirty

	def isDirty(self):
		return self.dirty

	def getFile(self):
		return self.file

	def getExportFile(self):
		return self.exportFile

	def nextID(self):
		return len(self.data)+1

	def isExportTermsToFileOK(self):
		r = False
		lang = gui.application.getLanguage()
		if self.exportFile and lang.getDoExport() and lang.getExportTemplate() and lang.getExportStatuses():
			statusList = ("|" + lang.getExportStatuses() + "|").replace("\\s", "")
			with open(self.exportFile, 'w', encoding=constants.ENCODING) as f:
				for t in self.data:
					if t:
						s = t.makeExportTemplateLine(statusList,lang.getExportTemplate())
						if s != "":
							f.write(s)
							#f.write(constants.EOL)
			r = True
		return r

	def isSaveTermsToFileOK(self):
		r = False
		if self.file:
			with open(self.file, 'w', encoding=constants.ENCODING) as f:
				for t in self.data:
					if t:
						f.write('%s%s' %(str(t), '\n'))
						#f.write(constants.EOL)
				r = True
				self.dirty = False
		return r

	def isSaveTermsToDBOK(self):
		r = False
		updatedWords = []
		updatedRoots = []
		newWords = []
		newRoots = []
		for t in self.data:
			if t:
				if t.updated:
					updatedWords.append(t.toUpdateSql())
				if t.root.updated:
					updatedRoots.append(t.root.toUpdateSql())
				if t.new:
					newWords.append(t.toSql())
				if t.root.new:
					newRoots.append(t.root.toSql())
		print(updatedRoots)
		import os
		try:
			conn = sqlite3.connect(self.db)
			langs = (self.dir,)
			if(len(newRoots) > 0):
				conn.executemany('INSERT INTO terms(language, word, definition, translation, priorSentence, sentenceCLOZE, sentence, followingSentence, source, status) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', newRoots)
			if(len(newWords) > 0):
				conn.executemany('INSERT INTO word(language, word, root, rootID) values (?, ?, ?, ?)', newWords)
			if(len(updatedRoots) > 0):
				conn.executemany('UPDATE terms SET definition = ?, translation = ?, priorSentence = ?, sentenceCLOZE = ? , sentence = ?, followingSentence = ?, source = ?, status = ? WHERE id = ?', updatedRoots)
			if(len(updatedWords) > 0):
				conn.executemany('UPDATE word SET root = ?, rootID = ? WHERE id = ?', updatedWords)
			if(len(self.deletedIDs) > 0):
				print(self.deletedIDs)
				conn.executemany('DELETE FROM word WHERE id = ?', self.deletedIDs)
			if(len(self.deletedRoots) > 0):
				conn.executemany('DELETE FROM terms WHERE id = ?', self.deletedRoots)
			conn.commit()
			conn.close()
			self.dirty = False
			r = True
		except BaseException as e:
			print('here e %s' %e)
			r = False
		self.dirty = False
		return r

#words
class Term():
	def __init__(self,  word, id, rootWord, rootID, new = True, updated = False):
		self.word = word
		self.root = rootWord
		self.key = self.word.lower()
		self.text = Text(text = word)
		self.rootID = rootID
		self.wordCount = len(self.text.getTextItems())
		self.new = new
		self.updated = updated
		self.id = id

	def toSql(self):
		return (gui.application.getLanguage().getLangName(), self.word,self.root.word,self.root.id)

	def toUpdateSql(self):
		return (self.root.word,self.root.id, self.id)

	def getStatus(self):
		return self.root.status

	def setStatus(self, status):
		self.root.status = status

	def getKey(self):
		return self.key

	def getWordCount(self):
		return self.wordCount

	def getText(self):
		return self.text

	def getTranslation(self):
		return self.root.translation

	def setTerm(self, term):
		self.word = term

	def setTranslation(self, trans):
		self.root.translation = trans

	def setSentence(self, sent):
		self.root.sentence = sent

	def displayWithStatusHTML(self):
		s = ""
		tr = self.root.definition
		if tr == "":
			tr = "(No Translation)"
		return utilities.escapeHTML('%s<br>root: %s<br>%s' %(self.word, self.root.word, utilities.escapeHTML('%s%s <br>%s — %s' %(s,tr, self.root.translation, self.root.status.getStatusShortText()))))

	def getTerm(self):
		return self.word

	def getSentence(self):
		return self.root.sentence

	def makeExportTemplateLine(self, statusList, exportTemplate):
		s = ""
		t = self
		status = "|" + str(t.getStatus().getStatusCode())+ "|"
		if (statusList.index(status) >= 0):
			s = exportTemplate
			s = s.replace("%w", t.getTerm())
			s = s.replace("%t", t.getTranslation())
			s = s.replace("%s", t.getSentence())
			s = s.replace("%c", t.getSentence()
					.replace("\\{.+?\\}", "{***}"))
			s = s.replace(
					"%d",
					t.getSentence().replace("\\{.+?\\}",
							"{***" + t.getTranslation() + "***}"))
			s = s.replace("%a", str(t.getStatus().getStatusCode()))
			s = s.replace("%k", t.getKey())
			s = s.replace("$w", utilities.escapeHTML(t.getTerm()))
			s = s.replace("$t", utilities.escapeHTML(t.getTranslation()))
			s = s.replace("$s", utilities.escapeHTML(t.getSentence()))
			s = s.replace(
					"$c",
					utilities.escapeHTML(t.getSentence().replace(
							"\\{.+?\\}", "{***}")))
			s = s.replace(
					"$d",
					utilities.escapeHTML(t.getSentence().replace(
							"\\{.+?\\}", "{***" + t.getTranslation() + "***}")))
			s = s.replace("$a", utilities.escapeHTML(str(t
					.getStatus().getStatusCode())))
			s = s.replace("$k", utilities.escapeHTML(t.getKey()))
			s = s.replace("\\t", "\t")
			s = s.replace("\\n", "\r\n")
			s = s.replace("$$", "$")
			s = s.replace("%%", "%")
			s = s.replace("\\\\", "\\")
		return s

	def __str__(self):
		return '%s%s%s%s%s%s%s%s%s' %(self.word, constants.TAB, self.root.definition, constants.TAB, self.root.translation, constants.TAB, self.root.sentence, constants.TAB, str(self.getStatus().getStatusCode()))


class RootWord():
	def __init__(self, id, word, definition, translation, priorSentence, sentenceCLOZE, sentence, followingSentence, source, status, new = True, updated = False):
		self.id = id
		self.word = word
		self.definition = definition
		self.translation = translation
		self.priorSentence = priorSentence
		self.sentenceCLOZE = sentenceCLOZE
		self.sentence = sentence
		self.followingSentence = followingSentence
		self.source = source
		self.status = TermStatus.getStatusFromCode(status)
		self.new = new
		self.updated = updated

	def toSql(self):
		#terms(language, word, definition, translation, priorSentence, sentenceCLOZE, followingSentence, source, status) values (?, ?, ?, ?, ?, ?, ?, ?, ?)', newWords)
		return (gui.application.getLanguage().getLangName(), self.word,self.definition, self.translation, self.priorSentence, self.sentenceCLOZE, self.sentence, self.followingSentence, self.source, self.status.getStatusCode())

	def toUpdateSql(self):
		#terms(language, word, definition, translation, priorSentence, sentenceCLOZE, followingSentence, source, status) values (?, ?, ?, ?, ?, ?, ?, ?, ?)', newWords)
		return (self.definition, self.translation, self.priorSentence, self.sentenceCLOZE, self.sentence, self.followingSentence, self.source, self.status.getStatusCode(), self.id)


from collections import OrderedDict
class TreeMap(OrderedDict):
	def __init__(self):
		super(TreeMap, self).__init__()