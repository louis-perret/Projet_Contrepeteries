from arbin import *
from filtre import *
from commun import *
from utilitaires import *
import string
import sys
import json
import re
import os

# ----------------------------------------------------------------------------
"""
Affiche les quadruplets trouvés suite à la recherche de façon jolie.
et permet de voir les orthographes différents des phonèmes du quadruplets en
appelant affiOrthoPhon
"""
def affiRechSon(listeAffichage, compteur, mot_origine,langue, dicoDico):
	dicoPhon = dicoDico['DicoPhon']
	motOriPhon = Mot_to_Phon_Only(arbre_mot, mot_origine) #On récupuère la syntaxe phonétique du mot d'origine
	listeAffichage = (sorted(listeAffichage, key=lambda lettre: lettre[0]))
	son1,son2 = "",""
	clear()
	nbMotPage = 25  # nombre de mots par pages
	nbPage = (len(listeAffichage)//nbMotPage)+1  # nombre total de pages.
	numPage = 1     
	while(True):
		compt = (numPage-1)*nbMotPage+1
		if listeAffichage != [] :
			min = (numPage-1)*nbMotPage
			if numPage == nbPage :
				max = len(listeAffichage)
			else :
				max = numPage*nbMotPage
			for pack in listeAffichage[min:max]: #pack = (lettre1,lettre2,mot1',mot2',mot2)

				espace = 40 - len(mot_origine) - len(pack[4])
				marge = len(str(compt))+2
				print(marge*" ", "Phonèmes", " "*(30-marge), "Un exemple d'orthographe")
				print(marge*" "+f"{motOriPhon} - {pack[4]}"+espace * " "+f"|  {mot_origine} - {dicoPhon[pack[4]][0]}")
				print(compt, 35 * " ", " ex : ")

				espace = 40 - len(pack[2]) - len(pack[3])

				print(marge*" "+f"{pack[2]} - {pack[3]}"+espace*" " +
					  f"|  {dicoPhon[pack[2]][0]} - {dicoPhon[pack[3]][0]}")

				print("\n"+"-"*60+"\n")

				son1 = pack[0]
				son2 = pack[1]
				compt += 1
			print("Échange entre : ",son1,"-",son2)
			print("page: "+str(numPage)+"/"+str(nbPage))
			print(f"Nombre de combinaisons : {len(listeAffichage)}")
		else :
			print("Aucun résultat\n")

		selecteur = None
		boucle = True
		while(boucle):
			try:
				selecteur = input(
					"\na: quitter l'aide\nz: revenir au début de l'aide\ne: page précédente\nr: page suivante\nou numéro du quadruplet, pour voir toutes les orthographes des phonèmes : \n")
			except:
				print("\nVous n'avez pas saisi un chiffre")
				continue

			if selecteur == "a":
				return 0
			elif selecteur == "z":
				clear()
				return 1
			elif selecteur == "r":
				numPage = numPage+1 if numPage+1 <= nbPage else numPage #Dépasse pas le nb page max
				boucle = False
			elif selecteur == "e":
				numPage = numPage-1 if numPage-1 >= 1 else numPage #Pas en dessous 1 page
				boucle = False
			elif inputInt(selecteur):
				selecteur = int(selecteur)
				if selecteur <= len(listeAffichage) and selecteur > 0:
					affiOrthoPhon(listeAffichage, selecteur-1, mot_origine,langue, dicoPhon)
					boucle = False
			else:
				print("\nL'entrée n'est pas valide, réessayez")


# ------------------------------------------------------------------------------
"""
Affiche toutes les orthographes contenus dans le dicoPhon.json des Phonèmes du quadruplet
de listeAffichage à l'index donnée en entrée.
"""


def affiOrthoPhon(listeAffichage, index, mot_origine,langue, dicoPhon):
	clear()

	motOriPhon = Mot_to_Phon_Only(arbre_mot, mot_origine)
	pack = listeAffichage[index]#Récupère le tuple voulu

	tCol = 20
	#affichage de l'écriture phonétique des 4 mots
	print(" "*8, motOriPhon, " "*(tCol-len(motOriPhon)), end='')
	print(pack[3], " "*(tCol-len(pack[4])), end='')
	print(pack[2], " "*(tCol-len(pack[2])), end='')
	print(pack[4], " "*(tCol-len(pack[3])), "\n")

	#On récupère tous les mots qui se prononcent pareil
	phon2 = dicoPhon[pack[3]] 
	phon3 = dicoPhon[pack[2]]
	phon4 = dicoPhon[pack[4]]

	for i in range(max((len(phon2), len(phon3), len(phon4)))):
		if i == 0:
			print(" "*7, mot_origine, " "*(tCol-len(motOriPhon)), end='')
		else:
			print(" "*8, " "*(tCol+1), end='')
		if i < len(phon2):
			print(phon2[i], " "*(tCol-len(phon2[i])), end='')
		else:
			print(" "*(tCol+1), end='')
		if i < len(phon3):
			print(phon3[i], " "*(tCol-len(phon3[i])), end='')
		else:
			print(" "*(tCol+1), end='')

		print(phon4[i]) if i < len(phon4) else print("")

	input("\nEntrez n'importe quel touche pour continuer ")


#---------------------------------------------------------------------

"""
Affichage intermédaire avant la fin.
Affiche les différentes tranches du phonème du mot d'origine qui peuvent
êtres remplacées pour former un mot dans le lexique
Retourne les sons que souhaite échangé l'utilisateur dans le mot d'origine
"""

def affiNbCorrTranche2(dicoSliceCom):
	# affichage du nombre de correspondances par tranche
	index = 1
	for i in dicoSliceCom.keys():
		# elimination des doublons dans les listes.
		dicoSliceCom[i] = sorted(list(set(dicoSliceCom[i])))
		tailleString = 15 - len(str(i) + str(len(dicoSliceCom[i])))

		print(index, i, "-"*tailleString+">", len(dicoSliceCom[i]), "mots")
		index += 1

	print("\n0 : quitter l'aide/ -1 revenir au début de l'aide")
	selectSlice = None
	test = True
	while(test):
		try:
			selectSlice = int(
				input("Quels sons voulez-vous voulez-vous échanger ? (rentrez leur indice) :"))
		except:
			print("")
		if selectSlice in range(1, len(dicoSliceCom.keys())+1):
			test = False
		elif selectSlice == 0:
			return 0
		elif selectSlice == -1:
			return -1
		else:
			print("L'entrée n'est pas valide, réessayez\n")
	return list(dicoSliceCom.keys())[selectSlice-1] #Récupère la liste des mots d'après l'échange selectionné


# -----------------------------------------------------------------------------
"""
Suite de affiNbCorrTranche2,
affiche page par page de 60 phonèmes avec un exemple d'orthographe
des mot possibles en échangeant les sons rentrée par l'utilisateur dans
la fonction précédante,
Retourne le phonème selectionné par l'utilisateur qui l'intéresse pour l'echange
"""

def affiPageParPage2(listeMot, syllOrigine, mot_origine):
	nbMotPage = 60  # nombre de mots par pages
	nbPage = (len(listeMot)//nbMotPage)  # nombre total de pages.
	numPage = 0                          # numéro page en cours

	with open('data/fr/dicoPhoncomFr.json') as tmp:
		dicoPhon = json.load(tmp)

	choix = {"r", "t"}
	selecteur = 0
	continuer = True
	while(continuer):
		if selecteur == -2:
			numPage = numPage+1 if numPage+1 <= nbPage else numPage
		elif selecteur == -1:
			numPage = numPage-1 if numPage-1 >= 0 else numPage

		clear()
		print(f"page {numPage}/{nbPage}\n")

		for i in range(1, nbMotPage, 2):

			mot1 = listeMot[nbMotPage*numPage+i-1] if nbMotPage*numPage+i-1 < len(listeMot) else ""
			mot2 = listeMot[nbMotPage*numPage+i] if nbMotPage*numPage+i < len(listeMot) else ""

			phon1 = "ex: "+dicoPhon[mot1][0] if mot1 != "" else ""
			phon2 = "ex: "+dicoPhon[mot2][0] if mot2 != "" else ""

			# recupération de la taille des mots pour l'espace entre les deux
			# c'est un pretty print
			espace1 = 15 - len(mot1)
			espace2 = 45 - len(phon1)-len(mot1)-espace1
			espace3 = 15 - len(mot2)

			if i <= 10:
				print(f"{i}  {mot1}", espace1*" ", phon1, " " *
					  espace2, f"{i+1}  {mot2}", espace3*" ", phon2)
			else:
				print(i, mot1, espace1*" ", phon1, " "*espace2, i+1, mot2, espace3*" ", phon2)

		print(
			f"\nLes mots obtenables en remplaçant '{syllOrigine}' dans '{Mot_to_Phon_Only(arbre_mot,mot_origine)}' ('{mot_origine}')")
		test = True
		while(test):

			try:
				selecteur = ("""
a : quitter l'aide\nz: revenir à selection précèdante\ne: revenir au début de l'aide
\nr:Gauche\nt:Droite\nou saisissez numéro du mot :\n""")
			except:
				print("\nVous n'avez pas saisi un chiffre")
				continue

			test1 = (nbMotPage*numPage+selecteur) <= len(listeMot) and (nbMotPage*numPage+selecteur) > 0
			if selecteur == "a":
				return 0
			elif selecteur == "z":
				clear()
				print(f"{mot_origine} : {Mot_to_Phon_Only(arbre_mot,mot_origine)}\n")
				return True
			elif selecteur == "e":
				return -1
			elif selecteur in choix or test1:
				print("\nChargement en cours ...")
				test = False
			else:
				print("\nL'entrée n'est pas valide, réessayez")
		continuer = False if selecteur not in choix else True
	return listeMot[nbMotPage*numPage+selecteur-1]
