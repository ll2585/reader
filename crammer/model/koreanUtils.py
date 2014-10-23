from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib

def getDefinition(word):
	u2 = urllib.parse.quote(word)
	url = 'http://endic.naver.com/search.nhn?sLn=en&isOnlyViewEE=N&query=%s' %(u2)
	print(url)
	page=urlopen(url)

	soup = BeautifulSoup(page.read())
	#check if this is a 1 pager
	div = soup.find(class_='fnt_k18')
	if div:
		term = div.strong.contents
		defs = div.find_next(class_='align_line')
		if(defs.a):
			defs.a.decompose()
		definition = str(defs.get_text(' ',strip=True))
		return (term, definition)
	#look for words/idioms section
	section = 'Words/Idioms'
	images = soup.find_all('img', alt=True)
	words = None
	for i in images:
		if(i['alt'] == section):
			words = i.find_previous(class_='word_num')
	if not words:
		return None
	possibleWords = words.find_all(class_='fnt_e30')
	if not possibleWords:
		return None
	found = False
	for w in possibleWords:
		if found:
			break
		for link in w.find_all('a'):
			l = link.get('href')
			if(l.find('/krenEntry.nhn?entryId')!= -1):
				div = link
				found = True
				break
	if not div:
		return None
	#else get the one that has stuff eg http://endic.naver.com/krenEntry.nhn?sLn=en&entryId=ee70e407172a440daef84629e6e8df8a&query=%EA%B7%B8
	term = div.strong.contents
	definition = div.find_next(class_='fnt_k05').get_text()
	return (term, definition)

#text = '그러나 더즐리 씨는 평상시와 똑같이, 부엉이가 없는 아침을 보냈다. 그는 직원 다섯 명에게 소리 소리를 질러댔으며, 중요한 전화 몇 통을 걸어 약간 더 거칠게 소리를 질렀다. '

#import re
#for t in re.sub("[^\w]", " ",  text).split():
#	print('%s: %s' %(t, get_root(t)))

#print(get_root('부엉이'))
