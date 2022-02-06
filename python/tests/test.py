import string
import numpy as np
import nltk

def fonction (y, a):
	listeMot = []
	for l in list(string.ascii_lowercase):
		if y == 1:
			print(f"{a+l}")
		else:
			fonction(y-1, a+l)

#fonction(3,'')


def FiltreTheme(mot,listeMotTheme):
	return mot in listeMotTheme

tab=['verbe','nom','proposition','adverbe']
print(FiltreTheme("adverbe",tab))


