from PyQt4 import QtGui, QtCore

from enum import Enum

colors = {}
lookupOrdinal = {}
lookup = {}
texts = {}
shorttexts = {}


class TermStatus(Enum):
	Null = 0
	Unknown = 1
	Learning2= 2
	Learning3 = 3
	Learning4 = 4
	Known = 5
	Ignored = 98
	WellKnown = 99


	def getStatusColor(self):
		if self in colors:
			return colors[self]
		else:
			return QtGui.QColor(255, 255, 255)

	def getStatusFromOrdinal(i):
		if i in lookupOrdinal:
			return lookupOrdinal[i]
		else:
			return TermStatus.Unknown

	def getStatusCode(self):
		return self.value

	def getStatusFromCode(i):
		if i in lookup:
			return lookup[i]
		else:
			return TermStatus.Unknown

	def getStatusShortText(self):
		if self in texts:
			return shorttexts[self]
		else:
			return "???"

	def getStatusText(self):
		if self in texts:
			return texts[self]
		else:
			return "???"

	def ordinal(self):
		for id, s in enumerate(list(TermStatus)):
			if s == self:
				return id

	def getAllActive():
		r = []
		for status in TermStatus:
			if status != TermStatus.Null:
				r.append(status)
		return r


colors[TermStatus.Null] = QtGui.QColor(180, 188, 255) # B4BCFF
colors[TermStatus.Unknown] = QtGui.QColor(245, 184, 169) # F5B8A9
colors[TermStatus.Learning2] = QtGui.QColor(245, 204, 169) # F5CCA9
colors[TermStatus.Learning3] = QtGui.QColor(245, 225, 169) # F5E1A9
colors[TermStatus.Learning4] = QtGui.QColor(245, 243, 169) # F5F3A9
colors[TermStatus.Known] = QtGui.QColor(197, 255, 197) # C5FFC5
colors[TermStatus.Ignored] = QtGui.QColor(229, 229, 229) # E5E5E5
colors[TermStatus.WellKnown] = QtGui.QColor(229, 255, 229) # E5FFE5


texts[TermStatus.Null] = "No status (%s)"%(TermStatus.Null.getStatusCode())
texts[TermStatus.Unknown] = "Unknown (%s)"%(TermStatus.Unknown.getStatusCode())
texts[TermStatus.Learning2] = "Learning (%s)"%(TermStatus.Learning2.getStatusCode())
texts[TermStatus.Learning3] = "Learning (%s)"%(TermStatus.Learning3.getStatusCode())
texts[TermStatus.Learning4] = "Learning (%s)"%(TermStatus.Learning4.getStatusCode())
texts[TermStatus.Known] = "Known (%s)"%(TermStatus.Known.getStatusCode())
texts[TermStatus.Ignored] = "Ignored (%s)"%(TermStatus.Ignored.getStatusCode())
texts[TermStatus.WellKnown] = "Well Known (%s)"%(TermStatus.WellKnown.getStatusCode())

shorttexts[TermStatus.Null] = "No status "
shorttexts[TermStatus.Unknown] = "Unknown"
shorttexts[TermStatus.Learning2] = "Learning/2"
shorttexts[TermStatus.Learning3] = "Learning/3"
shorttexts[TermStatus.Learning4] = "Learning/4"
shorttexts[TermStatus.Known] = "Known/5"
shorttexts[TermStatus.Ignored] = "Ignored"
shorttexts[TermStatus.WellKnown] = "Well Known"


for id, s in enumerate(list(TermStatus)):
	lookupOrdinal[id] = s
	lookup[s.value] = s