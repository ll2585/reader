import os
import app.constants as constants
import gui.utilities as utilities
from app.text import Text as Text
from app.TermStatus import TermStatus as TermStatus
import gui.application
import sqlite3


def lastIndexOf(arr, item):
    for i in range(len(arr) - 1, -1, -1):
        if item == arr[i]:
            return i
        else:
            raise ValueError("rindex(lis, item): item not in lis")


class Terms:
    def __init__(self):
        self.data = []
        self.keyIndex = {}
        self.keyIndex2 = {}
        self.exportFile = None
        self.file = None
        self.dirty = False
        self.db = ''
        self.dir = ''
        self.lemma_dict = {}
        self.term_dict = {}
        self.deletedIDs = []
        self.deletedRoots = []
        self.lemma_id_dict = {}
        self.term_id_dict = {}
        # TODO: delete self.term_dict and change this to self.term_dict once you clean up self.term_dict
        self.real_term_dict = {}
        # TODO: delete self.lemma_dict and change self.real_lemma_dict to self.lemma_dict
        self.real_lemma_dict = {}
        self.next_term_id = -1
        self.next_lemma_id = -1
        self.joined_info = []
        self.removed_links = []
        self.edited_notes = []
        self.tags = []

    def add_removed_link(self, term_id, lemma_id):
        self.removed_links.append({'term_id': term_id, 'lemma_id': lemma_id})
        self.setDirty(True)

    def is_load_terms_from_db_ok(self, db_path):
        self.db = db_path
        lang = gui.application.getLanguage().getLangName()
        try:
            conn = sqlite3.connect(db_path)
            lemmas = conn.execute('SELECT * from lemmas WHERE language = ?', (lang,)).fetchall()
            terms = conn.execute('SELECT * from terms WHERE language = ?', (lang,)).fetchall()
            lemmas_terms = conn.execute('SELECT * from lemmas_terms WHERE language = ?', (lang,)).fetchall()
            max_lemma_id = -1
            for w in lemmas:
                lemma_id = w[0]
                lemma = w[2]
                max_lemma_id = lemma_id if lemma_id > max_lemma_id else max_lemma_id
                # (self, id, word, definition, translation, priorSentence, sentenceCLOZE, sentence, followingSentence, source, status, new = True, updated = False):
                new_lemma = Lemma(w[0], w[2], w[3], w[4], w[5], w[6], w[7], w[8], w[9], w[10], new=False, updated=False)
                # TODO: replace real_lemma_dict with lemma_dict
                if lemma not in self.real_lemma_dict:
                    self.real_lemma_dict[lemma] = []
                self.real_lemma_dict[lemma].append(new_lemma)  # 1 to many
                self.lemma_id_dict[lemma_id] = new_lemma

                # TODO: delete this shit
                self.lemma_dict[lemma] = new_lemma  # 1 to 1
            self.next_lemma_id = max_lemma_id + 1
            max_term_id = -1
            for w in terms:
                term_id = w[0]
                max_term_id = term_id if term_id > max_term_id else max_term_id
                # TODO: this is where you might wanna have the shit about sentence, following sentence, cloze, etc. but for now fuck it
                # TODO: also here is where you delete shit like rootWord but w.e it should just be id, language, term
                new_term = Term(w[2], term_id, None, None, new=False, updated=False)
                self.add_term(new_term)
            self.next_term_id = max_term_id + 1
            for w in lemmas_terms:
                # lemma_id, term_id, language, notes
                info_dict = {'lemma_id': w[0], 'language': w[2], 'notes': w[3]}
                term_id = w[1]
                # we already added the terms to the dicts so should be there...
                if term_id in self.term_id_dict:
                    term = self.term_id_dict[term_id]
                    term.add_possible_lemma(info_dict)
                else:
                    print("Why is this term id {0} not in the terms dict?".format(term_id))
            # data.trimToSize()
            self.dirty = False
            r = True
        except BaseException as e:
            print(e)
            self.dirty = True
            r = False
        return r

    def getUnknownCards(self):
        unknownCards = []
        for t in self.lemma_dict:
            if self.lemma_dict[t].status not in [TermStatus.WellKnown, TermStatus.Ignored]:
                unknownCards.append(self.lemma_dict[t])
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
            # do multiwords later
            ## self.keyIndex2[firstWord][l][index] = None
            self.dirty = True
            idTuple = (t.id,)
            print(idTuple)
            self.deletedIDs.append(idTuple)

    def deleteRoot(self, lemma):
        if lemma in self.lemma_dict:
            rootTerm = self.lemma_dict[lemma]
            del self.lemma_dict[lemma]
            self.dirty = True
            idTuple = (rootTerm.id,)
            self.deletedRoots.append(idTuple)

    def add_term(self, t):
        # this key shit basically makes a dict for 1: 1 word terms, 2: 2 word terms starting with the term, 3: 3 word terms, etc.
        if t.getKey() in self.keyIndex.keys():
            self.data[self.keyIndex[t.getKey()]] = t
        else:
            self.data.append(t)
            index = lastIndexOf(self.data, t)
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
        if not t.word in self.term_dict:
            self.term_dict[t.word] = t

        # TODO: this is where we do the new shit
        term = t.get_term()
        term_id = t.id
        if not term_id in self.term_id_dict:
            self.term_id_dict[term_id] = t
        if not term in self.real_term_dict:
            self.real_term_dict[term] = []
        self.real_term_dict[term].append(t)

        self.dirty = True

    def match(self, text, index):
        nextIndex = -1
        ti = text.getTextItems()[index]
        debug = ti.textItemValue == '마법사의'
        if ti.getTextItemLowerCaseValue() in self.real_term_dict:
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
        return len(self.data) + 1

    def get_next_term_id_and_increment(self):
        to_return = self.next_term_id
        self.next_term_id += 1
        return to_return

    def get_next_lemma_id_and_increment(self):
        to_return = self.next_lemma_id
        self.next_lemma_id += 1
        return to_return

    def add_edited_notes(self, term_id, lemma_id, notes):
        self.edited_notes.append({'term_id': term_id, 'lemma_id': lemma_id, 'notes': notes})

    def isExportTermsToFileOK(self):
        r = False
        lang = gui.application.getLanguage()
        if self.exportFile and lang.getDoExport() and lang.getExportTemplate() and lang.getExportStatuses():
            statusList = ("|" + lang.getExportStatuses() + "|").replace("\\s", "")
            with open(self.exportFile, 'w', encoding=constants.ENCODING) as f:
                for t in self.data:
                    if t:
                        s = t.makeExportTemplateLine(statusList, lang.getExportTemplate())
                        if s != "":
                            f.write(s)
                        # f.write(constants.EOL)
            r = True
        return r

    def isSaveTermsToFileOK(self):
        r = False
        if self.file:
            with open(self.file, 'w', encoding=constants.ENCODING) as f:
                for t in self.data:
                    if t:
                        f.write('%s%s' % (str(t), '\n'))
                    # f.write(constants.EOL)
                r = True
                self.dirty = False
        return r

    def isSaveTermsToDBOK(self):
        r = False
        new_joins = []
        updated_lemmas = []
        new_terms = []
        new_lemmas = []
        removed_links = []
        for id, t in self.term_id_dict.items():
            if t.new:
                print(t)
                new_terms.append(t.to_sql())
        # TODO: allow for deleting joins lol...
        for new_join in self.joined_info:
            new_joins.append((new_join['lemma_id'], new_join['term_id'], new_join['language'], new_join['notes']))
        for id, lemma in self.lemma_id_dict.items():
            if lemma.updated:
                updated_lemmas.append(lemma.to_update_sql())
            if lemma.new:
                new_lemmas.append(lemma.to_sql())
        for d in self.removed_links:
            removed_links.append((d['lemma_id'], d['term_id']))
        print(self.edited_notes)
        import os
        try:
            conn = sqlite3.connect(self.db)
            langs = (self.dir,)
            print(self.edited_notes)
            if (len(new_lemmas) > 0):
                conn.executemany(
                    'INSERT INTO lemmas(language, lemma, definition, translation, priorSentence, sentenceCLOZE, sentence, followingSentence, source, status) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    new_lemmas)
            if (len(new_terms) > 0):
                conn.executemany('INSERT INTO terms(language, term, root, rootID) values (?, ?, ?, ?)', new_terms)
            if (len(updated_lemmas) > 0):
                conn.executemany(
                    'UPDATE lemmas SET definition = ?, translation = ?, priorSentence = ?, sentenceCLOZE = ? , sentence = ?, followingSentence = ?, source = ?, status = ? WHERE id = ?',
                    updated_lemmas)
            if (len(new_joins) > 0):
                conn.executemany('INSERT INTO lemmas_terms(lemma_id, term_id, language, notes) values (?, ?, ?, ?)',
                                 new_joins)
            if (len(self.deletedIDs) > 0):
                print(self.deletedIDs)
                conn.executemany('DELETE FROM terms WHERE id = ?', self.deletedIDs)

            if (len(self.deletedRoots) > 0):
                conn.executemany('DELETE FROM lemmas WHERE id = ?', self.deletedRoots)
            if (len(removed_links) > 0):
                for r in self.removed_links:
                    conn.execute('DELETE FROM lemmas_terms WHERE lemma_id=:lemma_id AND term_id=:term_id', r)
            if (len(self.edited_notes) > 0):
                for r in self.edited_notes:
                    conn.execute('UPDATE lemmas_terms SET notes=:notes WHERE lemma_id=:lemma_id AND term_id=:term_id',
                                 r)
            conn.commit()
            conn.close()
            self.dirty = False
            r = True
        except BaseException as e:
            print('here e %s' % e)
            r = False
        self.dirty = False
        return r


# words
class Term():
    def __init__(self, word, id, lemma, rootID, new=True, updated=False):
        self.word = word
        self.root = lemma
        self.key = self.word.lower()
        self.text = Text(text=word)
        self.rootID = rootID
        self.wordCount = len(self.text.getTextItems())
        self.new = new
        self.updated = updated
        self.id = id
        self.possible_lemmas = []

    def add_possible_lemma(self, info_dict):
        # info_dict is probably {lemma_id: id, notes: notes}
        self.possible_lemmas.append(info_dict)

    def get_possible_lemma_number(self, index):
        terms = gui.application.getTerms()
        lemma_id = self.possible_lemmas[index]['lemma_id']
        lemma = terms.lemma_id_dict[lemma_id]
        return lemma

    def get_first_possible_lemma(self):
        return self.get_possible_lemma_number(0)

    def add_new_lemma(self, lemma_id, language, notes):
        return self.add_possible_lemma({"lemma_id": lemma_id, "language": language, "notes": notes})

    def get_possible_lemmas(self):
        return [x['lemma_id'] for x in self.possible_lemmas]

    def get_notes_of_lemma_id(self, lemma_id):
        for possible_lemma in self.possible_lemmas:
            if possible_lemma['lemma_id'] == lemma_id:
                return possible_lemma['notes']
        return ''

    def to_sql(self):
        return (gui.application.getLanguage().getLangName(), self.word, self.get_first_possible_lemma().word,
                self.get_first_possible_lemma().id)

    def get_status(self):
        # TODO: replace so it's not always the first
        if len(self.possible_lemmas) > 0:
            first_lemma = self.possible_lemmas[0]
            terms = gui.application.getTerms()
            lemma = terms.lemma_id_dict[first_lemma['lemma_id']]
            return lemma.status
        return TermStatus.Null

    def setStatus(self, status):
        # TODO: replace so it's not always the first
        if len(self.possible_lemmas) > 0:
            first_lemma = self.possible_lemmas[0]
            terms = gui.application.getTerms()
            lemma = terms.lemma_id_dict[first_lemma['lemma_id']]
            lemma.status = status
        else:
            raise Exception('Impossible to set status with no lemma')

    def set_status_of_lemma_id(self, status, lemma_id):
        if self.has_lemma_id(lemma_id):
            terms = gui.application.getTerms()
            lemma = terms.lemma_id_dict[lemma_id]
            lemma.updated = True
            lemma.status = status
        else:
            raise Exception('Term {0} does not have lemma id {1}'.format(self.word, lemma_id))

    def getKey(self):
        return self.key

    def getWordCount(self):
        return self.wordCount

    def getText(self):
        return self.text

    def set_notes_of_lemma_id(self, notes, lemma_id):
        for possible_lemma in self.possible_lemmas:
            if possible_lemma['lemma_id'] == lemma_id:
                possible_lemma['notes'] = notes

    def get_translation(self):
        # TODO: replace so it's not always the first
        if len(self.possible_lemmas) > 0:
            first_lemma = self.possible_lemmas[0]
            terms = gui.application.getTerms()
            lemma = terms.lemma_id_dict[first_lemma['lemma_id']]
            return lemma.translation
        return "No Lemma"

    def setTerm(self, term):
        self.word = term

    def set_translation_of_lemma_id(self, translation, lemma_id):
        if self.has_lemma_id(lemma_id):
            terms = gui.application.getTerms()
            lemma = terms.lemma_id_dict[lemma_id]
            lemma.updated = True
            lemma.translation = translation
        else:
            raise Exception('Term {0} does not have lemma id {1}'.format(self.word, lemma_id))

    def has_lemma_id(self, lemma_id):
        for possible_lemma in self.possible_lemmas:
            if possible_lemma['lemma_id'] == lemma_id:
                return True
        return False

    def didnt_originally_have_lemma(self, lemma_id):
        return not self.has_lemma_id(lemma_id)

    def set_sentence_of_lemma_id(self, sentence, lemma_id):
        if self.has_lemma_id(lemma_id):
            terms = gui.application.getTerms()
            lemma = terms.lemma_id_dict[lemma_id]
            lemma.updated = True
            lemma.sentence = sentence
        else:
            raise Exception('Term {0} does not have lemma id {1}'.format(self.word, lemma_id))

    def display_with_status_html(self):
        # TODO: change to not always the first
        if len(self.possible_lemmas) > 0:
            first_lemma = self.possible_lemmas[0]
            terms = gui.application.getTerms()
            lemma = terms.lemma_id_dict[first_lemma['lemma_id']]
            lemma_text = lemma.word
            translation = lemma.translation
            definition = lemma.definition
            status = lemma.status.getStatusShortText()
            result = utilities.escapeHTML('{0}<br>lemma: {1}<br>{2}'.format(self.word, lemma_text, utilities.escapeHTML(
                '{0}<br>{1} — {2}'.format(definition, translation, status))))
        else:
            lemma_text = "(No Lemma)"
            translation = ""
            definition = ""
            status = ""
            result = utilities.escapeHTML('{0}<br>lemma: {1}'.format(self.word, lemma_text))
        return result

    def get_term(self):
        return self.word

    def get_sentence(self):
        # TODO: make so not first
        if len(self.possible_lemmas) > 0:
            first_lemma = self.possible_lemmas[0]
            terms = gui.application.getTerms()
            lemma = terms.lemma_id_dict[first_lemma['lemma_id']]
            return lemma.sentence
        return "No Lemma"

    def makeExportTemplateLine(self, statusList, exportTemplate):
        s = ""
        t = self
        status = "|" + str(t.get_status().getStatusCode()) + "|"
        if (statusList.index(status) >= 0):
            s = exportTemplate
            s = s.replace("%w", t.get_term())
            s = s.replace("%t", t.get_translation())
            s = s.replace("%s", t.get_sentence())
            s = s.replace("%c", t.get_sentence()
                          .replace("\\{.+?\\}", "{***}"))
            s = s.replace(
                "%d",
                t.get_sentence().replace("\\{.+?\\}",
                                         "{***" + t.get_translation() + "***}"))
            s = s.replace("%a", str(t.get_status().getStatusCode()))
            s = s.replace("%k", t.getKey())
            s = s.replace("$w", utilities.escapeHTML(t.get_term()))
            s = s.replace("$t", utilities.escapeHTML(t.get_translation()))
            s = s.replace("$s", utilities.escapeHTML(t.get_sentence()))
            s = s.replace(
                "$c",
                utilities.escapeHTML(t.get_sentence().replace(
                    "\\{.+?\\}", "{***}")))
            s = s.replace(
                "$d",
                utilities.escapeHTML(t.get_sentence().replace(
                    "\\{.+?\\}", "{***" + t.get_translation() + "***}")))
            s = s.replace("$a", utilities.escapeHTML(str(t
                                                         .get_status().getStatusCode())))
            s = s.replace("$k", utilities.escapeHTML(t.getKey()))
            s = s.replace("\\t", "\t")
            s = s.replace("\\n", "\r\n")
            s = s.replace("$$", "$")
            s = s.replace("%%", "%")
            s = s.replace("\\\\", "\\")
        return s

    def __str__(self):
        return '%s%s%s%s%s%s%s%s%s' % (
        self.word, constants.TAB, self.get_first_possible_lemma().definition, constants.TAB,
        self.get_first_possible_lemma().translation, constants.TAB, self.get_first_possible_lemma().sentence,
        constants.TAB, str(self.get_status().getStatusCode()))


class Lemma:
    def __init__(self, id, word, definition, translation, priorSentence, sentenceCLOZE, sentence, followingSentence,
                 source, status, new=True, updated=False):
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

    def to_sql(self):
        # terms(language, word, definition, translation, priorSentence, sentenceCLOZE, followingSentence, source, status) values (?, ?, ?, ?, ?, ?, ?, ?, ?)', newWords)
        return (
        gui.application.getLanguage().getLangName(), self.word, self.definition, self.translation, self.priorSentence,
        self.sentenceCLOZE, self.sentence, self.followingSentence, self.source, self.status.getStatusCode())

    def to_update_sql(self):
        # terms(language, word, definition, translation, priorSentence, sentenceCLOZE, followingSentence, source, status) values (?, ?, ?, ?, ?, ?, ?, ?, ?)', newWords)
        return (self.definition, self.translation, self.priorSentence, self.sentenceCLOZE, self.sentence,
                self.followingSentence, self.source, self.status.getStatusCode(), self.id)

    def new_empty_lemma(self):
        return Lemma(-1, '', '', '', self.priorSentence, self.sentenceCLOZE, self.sentence, self.followingSentence,
                     self.source, 1)


class Tag:
    def __init__(self, tag_id, tag_name, display_description, notes=''):
        self.tag_id = tag_id
        self.tag_name = tag_name
        self.display_description = display_description
        self.notes = notes


from collections import OrderedDict


class TreeMap(OrderedDict):
    def __init__(self):
        super(TreeMap, self).__init__()
