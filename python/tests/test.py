import string
import numpy as np


listeretour= [["la","là","lacs"],["poule","poules","pool","pools"]]
listeRes=[]
for mot in listeretour[0]:
		for mot2 in listeretour[1]:
			listeRes.append(mot + " " + mot2)

print(listeRes)

"""
def(listeRes,indice,nbMots):
	if(indice == nbMots):
			liste
	for(mot in listeretour[indice]):
		listeRe += "" + mot

def(listeRes,indice,nbMots):
"""

