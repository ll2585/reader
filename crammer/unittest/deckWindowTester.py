import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from crammer.gui import gui

class GuiTester(unittest.TestCase):
	def setUp(self):
		'''Create the GUI'''
		self.app = QApplication(sys.argv)
		self.form = gui.DeckWindow("test.csv")

	def test_demo(self):
		self.assertEqual(self.form.mainWidget.numCards(), 8)

	def test_knowZero(self):
		nextButton = self.form.mainWidget.nextButton
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		resultsWidget = self.form.centralWidget()
		self.assertTrue('0/8' in resultsWidget.knownLabel.text())

	def test_know5(self):
		nextButton = self.form.mainWidget.nextButton
		knownBox = self.form.mainWidget.knownCheckbox
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownBox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownBox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownBox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownBox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownBox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		resultsWidget = self.form.centralWidget()
		self.assertTrue('5/8' in resultsWidget.knownLabel.text())

	def test2Restart(self):
		nextButton = self.form.mainWidget.nextButton
		knownBox = self.form.mainWidget.knownCheckbox
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownBox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownBox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		resultsWidget = self.form.centralWidget()
		restartButton = resultsWidget.restartButton
		QTest.mouseClick(restartButton, Qt.LeftButton)
		mainWidget = self.form.centralWidget()
		self.assertTrue('1/6' in mainWidget.cardLabel.text())

	def testRestartAll(self):
		nextButton = self.form.mainWidget.nextButton
		knownBox = self.form.mainWidget.knownCheckbox
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownBox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownBox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		resultsWidget = self.form.centralWidget()
		restartAllButton = resultsWidget.restartAllButton
		QTest.mouseClick(restartAllButton, Qt.LeftButton)
		mainWidget = self.form.centralWidget()
		self.assertTrue('1/8' in mainWidget.cardLabel.text())

class ModelTester(unittest.TestCase):
	def setUp(self):
		'''Create the Model'''
		from crammer.model.model import Deck
		self.deckNoCards = Deck()
		self.deckCards = Deck("test.csv")

	def testEmptyDeck(self):
		self.assertEqual(self.deckNoCards.size(), 0)

	def testImportedDeck(self):
		self.assertEqual(self.deckCards.size(), 8)

	def testSubsetDeck(self):
		for deck in self.deckCards.subDeck():
			self.assertEqual(deck.size(), 8)
		shuffledCards = self.deckCards.shuffledCards()
		for deck in shuffledCards.subDeck():
			self.assertEqual(deck.size(), 8)

if __name__ == "__main__":
	unittest.main()