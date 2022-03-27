from arbin import *
from filtre import *
from commun import *
from utilitaires import *
import string
import sys
import json
import re
import os
from tempsExecution import * 

#les afficheurs encollent les murs (a faire mélange de lettres et phonème)
#l'apache recrute
#la flutiste fait peur
#je n'ai pas de rebords à mes épaulettes

# ----------------------------------------------------------------------------
"""
Objectif : Renvoie une liste des contrepétries possibles en remplaçant x par y lettres ou phonèmes
Paramètres :
	-Entrée :
		-mot : mot de base
		-x : nombre de lettres dans mot à changer
		-y : nombre de lettres pour la combinaison
		-mode : précise le type d'échange (word = lettre à lettre,son=phonème à phonème)
	-Sortie : 
		-listeMotCop : liste des réponses

listeMotCop est de la forme : (nouveau mot, ancienne(s) lettre(s), nouvelle(s) lettre(s))

Complexité = O((26^y)*N) où N est la longueur du mot, et 26^y la longueur des combinaisons (si on veut échanger par 3 lettres, on aura 26^3)
"""
def aide(mot,x,y,mode,langue,dicoDico):
	classGramMotOrigine=dicoDico["DicoGram"][mot]
	if(mode=="phon"): #Seulement échanger des sons
		dicoPhon = dicoDico['DicoPhon'] #récupère le dico des phonèmes
		phon_file = open(f"data/{langue}/BD_phoneme{langue.capitalize()}.txt", encoding="utf-8")
		BD_phoneme = phon_file.read()
		BD_phoneme = BD_phoneme.split("\n")
		#del BD_phoneme[-1] #Enlève le caractère vide de la fin du tableau
		listeSource=BD_phoneme
		mot = Mot_to_Phon_Only(arbre_mot, mot) #On récupère l'écriture phonétique du mot
	if(mode=="word"): #S'il veut seulement échanger des lettres
		listeSource=list(string.ascii_lowercase)

	dicoPhon=dicoDico['DicoPhon']
	dicoGram=dicoDico['DicoGram']
	listeDico=dicoDico['Themes']
	listeMotCop=[]

	listeCouple=recupCoupleLettre(y,'',[],listeSource) #Récupère la liste de combinaisons possibles de longueur y
	for lettre in enumerate(mot): #Pour chaque lettre du mot
		coupleLettre=recupCouple(mot,x,lettre[0]) #on recupère le prochain couple de lettre à échanger
		if coupleLettre[0]: #S'il existe un couple possible à échanger		
			for couple in listeCouple: #Pour chaque combinaison possible
				nvtMot=replacer(mot,couple,lettre[0],x) #On remplace
				if coupleLettre[1] != couple and isInDico(mode, nvtMot): #Si le mot existe et si on n'a pas remplacer par les mêmes lettres
					if (filtreTheme(nvtMot,listeDico,dicoDico['config']['Themes']) and gramFiltre(classGramMotOrigine,nvtMot,mode,dicoGram,dicoPhon,dicoDico['config']) and verifPluriel(nvtMot,dicoDico["DicoGram"],dicoDico["pluriel"], mode)):
						if(mode=='phon'):
							listeMotCop.append((nvtMot,coupleLettre[1],couple,dicoPhon[nvtMot][0]))
						if(mode=='word'):
							listeMotCop.append((nvtMot,coupleLettre[1],couple,mode))
						#circulaire(coupleLettre[1], couple, nvtMot, x)
				if dicoDico['config']['MotCoupe'] == "Oui":
					if(mode=='phon'):
						listeMotCop.extend(verificationEspace(nvtMot, coupleLettre[1], couple, mode, dicoPhon))
					if(mode=='word'):
						listeMotCop.extend(verificationEspace(nvtMot, coupleLettre[1], couple, mode, None))
	return listeMotCop

#---------- a enlever plus tard
def verifPluriel (mot, dicogram, dicoplur,mode):
	testC = False
	testP = True
	if(mode == "phon"):
		return True
	for classe in dicogram[mot.lower()]:
		if classe == "verbe" :
			testC = True
	if dicoplur[mot] == "p":
		testP = False
	return testC and testP


#-----------------------------------------------------------------------------
"""
effectue la recherche de quadruplet de manière générale
"""
def aideRechDicoGeneral(mot_origine, index, listeDeMotCop, minimum, maximum, dicoDico, mode):
	index -= 1
	NombreDeMot = len(listeDeMotCop)
	compteur = 0
	listeDeMotNONCop = []
	listeDeRacines = []
	listeAffichage = []
	# config filtres

	langue = dicoDico['config']['langue']
	tsv_file = open(f"data/{langue}/dico{langue.capitalize()}.csv", encoding="utf-8")
	lignes = csv.reader(tsv_file, delimiter=",")

	listeDico=[] #liste qui contiendra les dictionnaires par thème sélectionnés par l'utilisateur
	dicoPhon=dicoDico['DicoPhon']
	dicoGram=dicoDico['DicoGram']
	listeDico=dicoDico['Themes']

	classGramMotOrigine=dicoDico["DicoGram"][mot_origine]
	print(f"Recherche des résultats. Patientez jusqu'à que la bar de progression atteigne les {longueurDico}\n")
	bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
	i=0
	for mot in lignes:
		i = i+1
		bar.update(i)
		if(not verifPluriel(mot[0],dicoGram, dicoDico["pluriel"],"word")):
			continue
		if mode == 'word' :
			mot = mot[0] #On recupère le mot qu'on veut tester
		elif mode == 'phon' :
			mot = mot[1]
		if(motIsInBorne(minimum,maximum,mot) and gramFiltre(classGramMotOrigine,mot,mode,dicoGram,dicoPhon,dicoDico['config'])):
			#for ChaqueLettre in range(len(listeDeMotCop)):
			if(True):
				test1 = listeDeMotCop[index][2] in mot #Si la nouvelle lettre du mot listeDeMotCop[ChaqueLettre][2] est dans le mot du dictionnaire
				test2 = mot[:5] not in listeDeRacines
				# Racines:
				if test1 and test2: #Si c'est la combinaison sélectionnée avant
					testDansMot = replacer(mot, listeDeMotCop[index][1],mot.index(listeDeMotCop[index][2]),len(listeDeMotCop[index][2])) #replacer dans mot, à partir de l'index de là où se situe la nouvelle lettre par l'ancienne lettre
					# la lettre est dans le mot
					if testDansMot != Mot_to_Phon_Only(arbre_mot, mot_origine) and isInDico(mode, testDansMot) and motIsInBorne(minimum,maximum,testDansMot) and gramFiltre(classGramMotOrigine,testDansMot,mode,dicoGram,dicoPhon,dicoDico['config']) and testDansMot != mot_origine:
						if mode == "phon" :
							testTheme1 = dicoPhon[testDansMot]
							testTheme2 = dicoPhon[mot]
						elif mode == "word" :
							testTheme1 = testDansMot
							testTheme2 = mot

						if (filtreTheme(testTheme1,listeDico,dicoDico['config']['Themes']) or filtreTheme(testTheme2,listeDico,dicoDico['config']['Themes'])): #mot de base grossié, mot trouvé grossié ou mot du dico grossié
							listeDeRacines.append(mot[:5])
							listeAffichage.append((listeDeMotCop[index][1],
											   listeDeMotCop[index][2],
											   listeDeMotCop[index][0],
											   testDansMot, mot))
						compteur += 1
	print("\n")
	return (listeAffichage, compteur)






# ----------------------------------------------------------------------------
"""
pretty print des resultats de l'aide sur les lettres et les syllabes.
"""


def affiRechLettre(listeAffichage, compteur, mot_origine):

	nbMotPage = 25  # nombre de mots par pages
	nbPage = (len(listeAffichage)//nbMotPage)+1  # nombre total de pages.
	numPage = 1                          # numéro page en cours
	listeAffichage = (sorted(listeAffichage, key=lambda lettre: lettre[0])) #key = fonction qui prend lettre en param et ressort lettre[0] -> la liste sera trié par rapport à ça

	continuer = True
	while(continuer):
		clear()
		compt = (numPage-1)*nbMotPage+1
		min = (numPage-1)*nbMotPage
		if numPage == nbPage :
			max = len(listeAffichage)
		else :
			max = numPage*nbMotPage
		for pack in listeAffichage[min:max]: #pack = (lettre1,lettre2,mot1',mot2',mot2)

			marge = len(str(compt))+2
			print(marge*" "+f"{mot_origine} - {pack[4]}")
			print(compt)
			print(marge*" "+f"{pack[2]} - {pack[3]}")
			print("\n"+"-"*30+"\n")
			compt = compt+1

		print("page: "+str(numPage)+"/"+str(nbPage))
		print(f"Nombre de combinaisons : {len(listeAffichage)}")

		selecteur = None
		boucle = True
		while(boucle):
			try:
				selecteur = input(
					"\na: quitter l'aide\nz: revenir au début de l'aide :\ne: page précédente\nr: page suivante : ")
				break
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
		elif selecteur == "e":
			numPage = numPage-1 if numPage-1 >= 1 else numPage #Pas en dessous 1 page

		else:
			print("\nL'entrée n'est pas valide, réessayez")


# -----------------------------------------------------------------------------
"""
Affichage intermédaire avant la fin.
Affiche les différentes tranches du mot d'origine qui peuvent êtres remplacées
pour former un mot dans le lexique
Retourne la tranche que souhaite échangé l'utilisateur dans le mot d'origine
"""


def affiNbCorrTranche(dicoSliceCom):
	# affichage du nombre de correspondances par slices
	index = 1
	for i in dicoSliceCom.keys():
		# elimination des doublons dans les listes.
		dicoSliceCom[i] = sorted(list(set(dicoSliceCom[i]))) #le set enlève les doublons, on convertit une liste ordonnée
		tailleString = 15 - len(str(i) + str(len(dicoSliceCom[i]))) #pour aligner dans l'affichage

		print(index, i, "-"*tailleString+">", len(dicoSliceCom[i]), "mots")
		index += 1

	print("\n0 : quitter l'aide/ -1 revenir au début de l'aide")
	selectSlice = None
	test = True
	while(test):
		try:
			selectSlice = int(
				input("Quelle partie voulez-vous voulez-vous échanger ? (rentrez leur indice) :"))
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
Suite de affiNbCorrTranche,
affiche page par page de 60 mots des mot possibles en échangeant la tranches
rentrée par l'utilisateur dans la fonction précédante,
Retourne le mot selectionné par l'utilisateur qui l'intéresse pour l'echange
"""


def affiPageParPage(listeMot, syllOrigine, mot_origine):
	nbMotPage = 60  # nombre de mots par pages
	nbPage = (len(listeMot)//nbMotPage)  # nombre total de pages.
	numPage = 0                          # numéro page en cours

	tailleLigne = 50
	choix = {"r", "t"}
	selecteur = 0
	continuer = True
	while(continuer):
		if selecteur == -2:
			numPage = numPage+1 if numPage+1 <= nbPage else numPage #Dépasse pas le nb page max
		elif selecteur == -1:
			numPage = numPage-1 if numPage-1 >= 0 else numPage #Pas en dessous 0 pages

		clear()
		print(f"page {numPage}/{nbPage}\n")

		for i in range(1, nbMotPage, 2): #de 1 à 60 avec un pas de 2

			mot1 = listeMot[nbMotPage*numPage+i-1] if nbMotPage*numPage+i-1 < len(listeMot) else ""
			mot2 = listeMot[nbMotPage*numPage+i] if nbMotPage*numPage+i < len(listeMot) else ""

			# recupération de la taille des mots pour l'espace entre les deux
			# c'est un pretty print
			tailleEspace = tailleLigne-len(mot1)

			if i <= 10:
				print(f"{i}  {mot1}", " "*tailleEspace, f"{i+1}  {mot2}")
			else:
				print(i, mot1, " "*tailleEspace, i+1, mot2)

		print(
			f"\nLes mots obtenables en remplaçant '{syllOrigine}' dans '{mot_origine}'")
		test = True
		while(test):

			try:
				selecteur = input("""
a : quitter l'aide\nz: revenir à selection précèdante\ne: revenir au début de l'aide
r:Gauche\nt:Droite\nou saisissez numéro du mot :\n""")
			except:
				print("\nVous n'avez pas saisi un chiffre")
				continue

			test1 = (nbMotPage*numPage+selecteur) <= len(listeMot) and (nbMotPage*numPage+selecteur) > 0 #Si je peux toujours afficher des mots

			if selecteur == "a":
				return 0
			elif selecteur == "z":
				clear()
				print(f"{mot_origine}\n")
				return True
			elif selecteur == "e":
				return -1
			elif selecteur in choix or test1:
				test = False
			else:
				print("\nL'entrée n'est pas valide, réessayez")
		continuer = False if selecteur not in choix else True
	return listeMot[nbMotPage*numPage+selecteur-1] #retourne le mot sélectionné par l'utilisateur pour l'échange


# ----------------------------------------------------------------------------
"""
Fait la liste des quaduplets d'échanges possibles:
de forme exemple :

(syll1,syll2,mot1',mot2',mot2)
"""

def aideSyllRechDico(mot_origine, selectMot, syllOrigine):
				 # d'an'se      d'ar'se    an

	listeAffichage = []
	listeTmp = []

	# recup deb et fin de mot_origine:
	debFin = mot_origine.split(syllOrigine) #séparent le mot avec la syllabe choisie
	# extraction de 'ar' de selectMot.
	if len(debFin[1]) > 0: #Si la longueur de la fin du mot > 0aideLettreRechDicoGeneral
		syllNvlle = selectMot[len(debFin[0]):-len(debFin[1])] #on récupère juste 'ar' dans 'darse'

	else:
		syllNvlle = selectMot[len(debFin[0]):] #on récupère juste 'ar' dans 'darse'
	print(syllNvlle,"-",syllOrigine)
	tsv_file = open("data/fr/dicoFr.csv", encoding="utf-8")
	LexLignes = csv.reader(tsv_file, delimiter=",")

	with open('data/DicoVulgaire.json') as vulgaire:
		BDvulgaire = json.load(vulgaire)

	with open('data/config.json') as diconfig_:
		diconfig = json.load(diconfig_)

	# lit ligne par ligne du DICO (près de 100k lignes)
	# changer filtres
	print('Maintenant il reste à gérer les filtres pour la génération')
	diconfig = changerfiltre(diconfig)

	for ligne in LexLignes:
		LexMot = ligne[0] #On récupère le mot du dico

		# cherche occurences de la nouvelle tranche dans le lexique
		if syllNvlle in LexMot:

			# on recupère le deb et fin du mot du lexique
			indexSyllNvlle = re.finditer(syllNvlle, LexMot) #retourne un itérateur
			indexSyllNvlle = [match.start() for match in indexSyllNvlle] 

			for i in indexSyllNvlle:
				# À partir de celles-ci on recupère le début et la fin de ce mot
				LexDeb = LexMot[:i]
				LexFin = LexMot[i+len(syllNvlle):]

				# on teste si le la concaténation du debut et fin de ce mot avec la slice
				# d'origine forment un mot qui existe dans le lexique
				testMot = LexDeb + syllOrigine + LexFin
				if isInDico('word', testMot) and testMot not in listeTmp:
					if diconfig["FiltreGrossier"] == "Oui":
						if (selectMot in BDvulgaire or testMot in BDvulgaire or LexMot in BDvulgaire):
							listeAffichage.append([syllOrigine, syllNvlle,
												   selectMot, testMot,
												   LexMot])
							listeTmp.append(testMot)
					else:

						# si oui on l'ajoute a notre liste de résultat.
						listeAffichage.append([syllOrigine, syllNvlle,
											   selectMot, testMot,
											   LexMot])
						listeTmp.append(testMot)
	return (listeAffichage, len(listeAffichage), diconfig)

# ----------------------------------------------------------------------------
"""
recherche et affichage rapide des contrepeteries dans un quadruplé prédefinie
"""

def quadruplRapide (mot):
	compteur = 0
	listeAffichage = []
	histo = []
	motSplit = mot.split('/')
	for i in range(len(motSplit[0])):
		for j in range(len(motSplit[1])):
			for lettre0 in enumerate(motSplit[0]):
				for lettre1 in enumerate(motSplit[1]):
					coupleLettre0=recupCouple(motSplit[0],i,lettre0[0])
					coupleLettre1=recupCouple(motSplit[1],j,lettre1[0])
					if coupleLettre0[0] and coupleLettre1[0]:
						nvMot0=replacer(motSplit[0],coupleLettre1[1],lettre0[0],i)
						nvMot1=replacer(motSplit[1],coupleLettre0[1],lettre1[0],j)
						if isInDico('word',nvMot0) and isInDico('word',nvMot1) :							
							if nvMot0 not in histo and nvMot1 not in histo and nvMot0 != motSplit[0] and nvMot0 != motSplit[1]:
								listeAffichage.append((coupleLettre0[1],coupleLettre1[1],nvMot0,nvMot1,motSplit[1]))
								histo.append(nvMot0)
								compteur += 1
	if listeAffichage != [] :
		return affiRechLettre(listeAffichage, compteur, motSplit[0])
						

"""
Objectif : Renvoie true si la longueur du mot correspond aux critères de l'utilisateur
Paramètres :
	-Entrée :
		-minimum : longueur minimum
		-maximum : longueur maximum
		-mot : mot à vérifier
	-Sortie : 
		un boolean
"""
def motIsInBorne(minimum,maximum,mot):
	if((minimum==-1 or len(mot)>=minimum) and (maximum==-1 or len(mot)<=maximum)):
		return True
	return False





