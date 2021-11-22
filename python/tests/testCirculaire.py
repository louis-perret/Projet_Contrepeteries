from arbin import *	
from filtre import *
import string
import sys
import json
import re
import os

#-----------------------------------------------------------------------------
"""
fonction générant des contrpèteries circulaires
"""

def circulaire (ancLettre, nouvLettre, nouvMot, x):
	listeSextup = []
	with open('data/config.json') as diconfig_:
		diconfig = json.load(diconfig_)
	tsv_file = open("data/Lexique383.tsv", encoding="utf-8")
	lignes = csv.reader(tsv_file, delimiter="\t")
	# lit ligne par ligne du DICO (près de 100k lignes)
	# changer filtres
	diconfig = changerfiltre(diconfig)
	# bd filtres
	with open('data/DicoVulgaire.json') as vulgaire:
		BDvulgaire = json.load(vulgaire)
	for mot in lignes:
		mot = mot[0]
		for l in enumerate(mot):
			nouvMot1 = replacer(mot, ancLettre, l[0], x)
			if isInDico('word', nouvMot1):
				midLettre = mot[l[0]:l[0]+x]
				for mot2 in lignes:
					if nouvLettre in mot2:
						for l2 in mot2:
							nouvMot2 = replacer(mot2, midLettre, l2[0], x)
							if isInDico('word', nouvMot2):
								listeSextup.append((ancLettre, midLettre, nouvLettre, mot, mot2, nouvMot, nouvMot1, nouvMot2))
	print(listeSextup)
	return listeSextup

