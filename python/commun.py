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
	else:
		if(mot[index] == "ː"):
			return (False,'')
	if(index < len(mot)-1):
		if(mot[index+1] == "ː"):
			if(x==1):
				x=x+1
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

Complexité : O(N^2)
"""

def verificationEspace(mot, ancienneLettre, nouvelleLettre, dico, dicoPhon):

	listeMot = []
	for l in enumerate(mot): #pour chaque lettre du mot
		if l[0] >= 2 and l[0] <= len(mot)-2: #bornes pour la taille minimum des mot (ici 2 lettres)
			motEspace1 = replacer(mot, ' ', l[0], 0) #ajout d'un espace
			motSplit = motEspace1.split(' ') #séparation des mots à l'espace
			if isInDico(dico, motSplit[0]) and isInDico(dico, motSplit[1]): #vérification des deux mots
				if dico == 'word' :
					listeMot.append((motEspace1, ancienneLettre, nouvelleLettre,dico))
				if dico == 'phon' :
					try : #alors... on test si les deux mots sont dans le dico juste avant mais ça arrive à passer à travers et génère une keyerror dans certains cas
						exemple = dicoPhon[motSplit[0]][0]+" "+dicoPhon[motSplit[1]][0]
						listeMot.append((motEspace1, ancienneLettre, nouvelleLettre,exemple))
					except(KeyError) : 
						continue
			for l in enumerate(motSplit[0]): #recherche dans le premier mot apres une séparation
				if l[0] >= 2 and l[0] <= len(motSplit[0])-2:
					motEspace2 = replacer(motSplit[0], ' ', l[0], 0) #ajout d'un espace
					motSplit2 = motEspace2.split(' ') #séparation des mots à l'espace
					if isInDico(dico, motSplit2[0]) and isInDico(dico, motSplit2[1]) and isInDico(dico, motSplit[1]): #vérification des deux mots
						if (motEspace2+' '+motSplit[1], ancienneLettre, nouvelleLettre) not in listeMot:
							if dico == 'word' :
								listeMot.append((motEspace2+' '+motSplit[1], ancienneLettre, nouvelleLettre,dico))
							if dico == 'phon' :
								exemple = dicoPhon[motSplit2[0]][0]+" "+dicoPhon[motSplit2[1]][0]+" "+dicoPhon[motSplit[1]][0]
								listeMot.append((motEspace2+' '+motSplit[1], ancienneLettre, nouvelleLettre,exemple))
			for l in enumerate(motSplit[1]): #recherche dans le second mot apres une séparation
				if l[0] >= 2 and l[0] <= len(motSplit[1])-2:
					motEspace3 = replacer(motSplit[1], ' ', l[0], 0) #ajout d'un espace
					motSplit3 = motEspace3.split(' ') #séparation des mots à l'espace
					if isInDico(dico, motSplit3[0]) and isInDico(dico, motSplit3[1]) and isInDico(dico, motSplit[0]): #vérification des deux mots
						if (motSplit[0]+' '+motEspace3, ancienneLettre, nouvelleLettre) not in listeMot:
							if dico == 'word' :
								listeMot.append((motSplit[0]+' '+motEspace3, ancienneLettre, nouvelleLettre,dico))
							if dico == 'phon' :
								exemple = dicoPhon[motSplit[0]][0]+" "+dicoPhon[motSplit3[0]][0]+" "+dicoPhon[motSplit3[1]][0]
								listeMot.append((motSplit[0]+' '+motEspace3, ancienneLettre, nouvelleLettre,exemple))
				
		
	return listeMot

#-------------------------------------------------------------------------
"""
fonction pour l'affichage dans le menu
"""
def affichageBase (mot,listeDeMotCop,x) : 
	if(len(listeDeMotCop) == 0):
		print("Aucun résultat pour cette recherche")
		return
	print('Voici donc les couples que l\'on peut changer : ')
	for lettre in enumerate(mot): #Pour chaque lettre du mot
		coupleLettre=recupCouple(mot,x,lettre[0])
		if coupleLettre[0]: #S'il existe un couple possible à échanger
			print(f'\'{coupleLettre[1]}\'',end=' ')
	print("\n")
	for i in enumerate(listeDeMotCop): #i[0] -> index, i[1][1] -> ancienne lettre, i[1][2] -> nouvelle lettre, i[1][0] -> nouveau mot
		tmp = i[1][2] if i[1][2] != "" else chr(32)
		if i[1][3] == 'word' :
			print(f" {i[0]+1}   {i[1][1]} - {tmp}    {i[1][0]}")
		else :
			print(f"{i[0]+1}  {i[1][1]} - {tmp}    {i[1][0]} ex : {i[1][3]}")


"""
Objectif : Effectue l'affichage du nombre de résultats par tranche du mot pour le mode 'plusieurs'
Paramètres :
	-Entrée :
		-mot : mot entré par l'utilisateur
		-dicoResWord : dico des résultats des échanges de lettres (clé -> longueur échangée)
		-dicoResWord : dico des résultats des échanges de phonèmes (clé -> longueur échangée)
	-Sortie : 
		aucun
"""
def affichageBasePlusieurs(mot,dicoResWord,dicoResPhon):
	print("Voici les résultats pour chaque échange possible dans le mot : " + mot)
	i=1
	print("Voici les résultats pour les échanges entre lettres :")
	for key in dicoResWord.keys():
		print(f"{i}   {key} lettre(s) -  x lettre(s) --> {len(dicoResWord[key])} résultats")
		i=i+1
	print("\n")
	print("Voici les résultats pour les échanges entre phonèmes : \n")
	for key in dicoResPhon.keys():
		print(f"{i}   {key} phonème(s) - x phonème(s) --> {len(dicoResPhon[key])} résultats")
		i=i+1




"""
Objectif : chercher des contrepèterie circulaires
Paramètres :
	-Entrée :
		x : taille enlevée
		y : taille du rajout
		w : nombre de mot dans la boucle
		dico : type du dictionnaire
		motDepart : mot de départ
		motPrec : mots précédents dans la boucle
		sylabe : sylabe échangée dans le mot de départ
		index : index de la sylabe échangée dans le mot de départ
	-Sortie :
		listeCirculaires : liste des contrepèterie circulaires fonctionelles 
"""

#def rechercheCirculaire (motDepart, x, y, w, dico, motPrec, sylabe, index):