import string
from arbin import *
from filtre import *
import sys
import json
import re
import os
import csv

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

#--------------------------------------------------------------------------

"""
fonction vérifiant si une contrepétries est valide avec des espaces
"""

def verificationEspace(mot, ancienneLettre, nouvelleLettre, dico):

	listeMot = []

	for l in enumerate(mot): #pour chaque lettre du mot
		if l[0] >= 2 and l[0] <= len(mot)-2: #bornes pour la taille minimum des mot (ici 2 lettres)
			motEspace1 = replacer(mot, ' ', l[0], 0) #ajout d'un espace
			motSplit = motEspace1.split(' ') #séparation des mots à l'espace
			if isInDico(dico, motSplit[0]) and isInDico(dico, motSplit[1]): #vérification des deux mots
				listeMot.append((motEspace1, ancienneLettre, nouvelleLettre,dico))
			for l in enumerate(motSplit[0]): #recherche dans le premier mot apres une séparation
				if l[0] >= 2 and l[0] <= len(motSplit[0])-2:
					motEspace2 = replacer(motSplit[0], ' ', l[0], 0) #ajout d'un espace
					motSplit2 = motEspace2.split(' ') #séparation des mots à l'espace
					if isInDico(dico, motSplit2[0]) and isInDico(dico, motSplit2[1]) and isInDico(dico, motSplit[1]): #vérification des deux mots
						if (motEspace2+' '+motSplit[1], ancienneLettre, nouvelleLettre) not in listeMot:
							listeMot.append((motEspace2+' '+motSplit[1], ancienneLettre, nouvelleLettre,dico))
			for l in enumerate(motSplit[1]): #recherche dans le second mot apres une séparation
				if l[0] >= 2 and l[0] <= len(motSplit[1])-2:
					motEspace3 = replacer(motSplit[1], ' ', l[0], 0) #ajout d'un espace
					motSplit3 = motEspace3.split(' ') #séparation des mots à l'espace
					if isInDico(dico, motSplit3[0]) and isInDico(dico, motSplit3[1]) and isInDico(dico, motSplit[0]): #vérification des deux mots
						if (motSplit[0]+' '+motEspace3, ancienneLettre, nouvelleLettre) not in listeMot:
							listeMot.append((motSplit[0]+' '+motEspace3, ancienneLettre, nouvelleLettre,dico))
				
		
	return listeMot

#-------------------------------------------------------------------------
"""
fonction pour l'affichage dans le menu
"""
def affichageBase (listeDeMotCop) : 
	for i in enumerate(listeDeMotCop): #i[0] -> index, i[1][1] -> ancienne lettre, i[1][2] -> nouvelle lettre, i[1][0] -> nouveau mot
		tmp = i[1][2] if i[1][2] != "" else chr(32)
		if i[1][3] == 'word' :
			print(f" {i[0]+1}   {i[1][1]} - {tmp}    {i[1][0]}")
		else :
			print(f"{i[0]+1}  {i[1][1]} - {tmp}    {i[1][0]} ex : {i[1][3]}")

"""
Objectif : Créer un fichier qui contient un dico : key -> une écriture phonétique, value -> toutes ses orthographes possibles
Paramètres :
	-Entrée :
		fichierSrc : fichier source
		fichierDest : fichier destination
	-Sortie :
		aucun
"""
def creerFichierPhon(fichierSrc,fichierDest):
	file = open(fichierSrc, encoding="utf-8")
	read_file = csv.reader(file, delimiter=",")
	dicoPhon={}
	for ligne in read_file:
		if(ligne[1] in dicoPhon):
			dicoPhon[ligne[1]].append(ligne[0])
		else:
			dicoPhon[ligne[1]]=list()
			dicoPhon[ligne[1]].append(ligne[0])
	with open(fichierDest,'w') as file2:
		json.dump(dicoPhon,file2)



"""
Objectif : Créer un fichier qui contient un dico : key -> un mot, value -> toutes ses classes grammaticales possibles
Paramètres :
	-Entrée :
		fichierSrc : fichier source
		fichierDest : fichier destination
	-Sortie :
		aucun
"""
def creerFichierClassGramm(fichierSrc,fichierDest):
	file = open(fichierSrc, encoding="utf-8")
	read_file = csv.reader(file, delimiter=",")
	dicoClassGramm={}
	for ligne in read_file:
		if(ligne[0] in dicoClassGramm):
			dicoClassGramm[ligne[0]]=ligne[3][2:-2].replace('\'','').split(',')
		else:
			dicoClassGramm[ligne[0]]=ligne[3][2:-2].replace('\'','').split(',')
	with open(fichierDest,'w') as file2:
		json.dump(dicoClassGramm,file2)

#creerFichierClassGramm("data/fr/dicoFr.csv","data/fr/dicoClassGrammFr.json")
#creerFichierPhon("data/fr/dicoFr.csv","data/fr/dicoPhoncomFr.json")