import string
from arbin import *
from filtre import *
import sys
import json
import re
import os

"""
Remplace une lettre dans la chaine s à la position "index"
par la chaîne newstring.
i.e replacer("bonjour","pate",3) --> "bonpateour"
"""


def replacer(s, newstring, index,length):
	
	if index < 0:  # l'ajoute au début
		return newstring + s
	if index > len(s):  # l'ajoute à la fin
		return s + newstring
		# insère la nouvelle chaîne entre les tranches de l'original
	return s[:index] + newstring + s[index + length:]

# ----------------------------------------------------------------------------

"""
Objectif : Renvoie un couple de x lettre(s) à partir de l'index index dans le mot mot
Paramètres :
	-Entrée :
		mot : mot sur lequel on va récupérer le couple
		x : nombre de lettres pour le couple
		index : à partir de qu'elle lettre
	-Sortie :
		Renvoie un tuple de la forme : boolean,couple.
"""
def recupCouple(mot,x,index):
	if x>1: #Si on désire récupérer un couple de plus de 2 lettres
		if index+(x-1) >= len(mot): #Si on est à la fin du mot (evite les index out of range)
			return (False,'') #Exemple : bonjour, si on est à la lettre r, on peut pas prendre de couple avec r car on est à la fin
	return (True,mot[index:index+x])
	
# ----------------------------------------------------------------------------

"""
Objectif : Renvoie une liste des couples possibles de lettres à partir de l'alphabet
Paramètres :
	-Entrée :
		-y : nombre lettres pour la combinaison
		-a : chaîne contenant la combinaison (utile pour la récursivité, vide au premier appel)
		-liste : liste des réponses (utile pour la récursivité, vide au premier appel)
	-Sortie : 
		-listeCouple : liste des réponses

Exemple : Si je désire récupérer tous les couples de 2 lettres possibiles à partir de l'alphabet, j'utilise cette fonction qui me retournera une liste qui contiendra : aa,ab,ac,ad,...,zz.
"""
def recupCoupleLettre(y,a,liste,listeSource):
	listeCouple=liste
	for l in listeSource:
		if y == 1: #On a le nombre de lettre désiré
			listeCouple.append(a+l)
		else:
			listeCouple=recupCoupleLettre(y-1,a+l,listeCouple,listeSource) 
	return listeCouple

