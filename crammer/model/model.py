class Card():
	def __init__(self, front, back):
		self.front = front
		self.back = back
		self.known = False

	def getFront(self):
		return self.front

	def getBack(self):
		return self.back

	def setStatus(self, status):
		self.known = status

	def getStatus(self):
		return self.known

	def setFront(self, front):
		self.front = front

	def setBack(self, back):
		self.back = back

class Deck():
	def __init__(self, f = None, cards = None):
		self.cards = [] if cards is None else cards
		if(f is not None):
			self.makeCards(f)

	def makeCards(self, f):
		import csv, codecs
		with codecs.open(f, 'r', encoding = 'utf8') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				c = Card(row[0], row[1])
				self.cards.append(c)

	def shuffledCards(self):
		import copy, random
		copiedCards = copy.deepcopy(self)
		random.shuffle(copiedCards.cards)
		return copiedCards

	def size(self):
		return len(self.cards)

	#returns an array of decks of size factor, except the last one
	def subDeck(self, factor = 8, cards = None):
		cardsToSubSet = cards if cards is not None else self.cards
		subset = [cardsToSubSet[i:i+factor] for i in range(0, len(cardsToSubSet), factor)]
		deckArray = []
		for s in subset:
			deckArray.append(Deck(cards = s))
		return(deckArray)

	def getCardAt(self, location):
		return self.cards[location]

	def knownCards(self):
		return sum(1 for x in self.cards if x.known)

	def getCards(self):
		return self.cards

	def restartAll(self):
		for c in self.cards:
			c.setStatus(False)



'''

def nextCard():
	global cardNumber
	cardNumber += 1

def previousCard():
	global cardNumber
	cardNumber -= 1

def curCardKnown():
	return deck[cardNumber].getStatus()

def setCardStatus(status):
	global deck
	deck[cardNumber].setStatus(status)

def loadCards(file):


	'''