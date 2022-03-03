import sys
import json
import os
from filtre import *
from arbin import *
from fonc_aide_son import *
from fonc_aide_lettre import *
from commun import *
from utilitaires import *

sys.stdout.reconfigure(encoding='utf-8')

"""
Objectif : Gère le mode aide à la contrepèterie
Paramètres :
	-Entrée :
		-dicoDico : dictionnaire contenant les fichiers + config de l'application
		-historique : historique des 5 derniers mots entrés par l'utilisateur
	-Sortie : 
		-historique : un tableau
"""
def aideContrepetrie(dicoDico,historique):
	with open('data/config.json','r') as diconfig_:
		dicoConfig = json.load(diconfig_)
		langue=dicoConfig['langue'] #on récupère la langue entrée par l'utilisateur
		dicoDico['config']=dicoConfig
	# boucle "tant que" pour le recommencer aide avec un autre mot.
	continuer = 1
	while continuer == 1:
		clear()
		mot=choixMot(historique) #choix du mot
		mot = mot.lower()
		#On update l'historique
		if mot in historique :
			historique.remove(mot)
		historique.insert(0,mot)
		if len(historique) == 6:
			historique.pop(-1)

		#Pour la recherche rapide entre deux mots de la forme : mot1/mot2
		if "/" in mot :
			quadruplRapide(mot)
			continue #Recommence au début du while


		listeDeMotCop = [] #contient les contrepétries du mot entré
		choix=choixMode() #sélection du mode

		clear()
		if(choix == "r" ):
			continuer=0
			continue

		elif choix == "a": #recherche personnalisée pour les lettres
			continuer=modePersonnalisé("word",mot,langue,dicoDico)

		elif choix == "z": #recherche personnalisée pour les sons
			continuer=modePersonnalisé("phon",mot,langue,dicoDico)

		elif choix == "e": #'nimporte quel nombre de lettre
			continuer=recherchePlusieurs(mot,langue,dicoDico)
	return historique


"""
Objectif : Gère le choix du mot de l'utilisateur
Paramètres :
	-Entrée :
		-historique : historique des 5 derniers mots entrés par l'utilisateur
	-Sortie : 
		le mot entré par l'utilisateur
"""
def choixMot(historique):
	if historique != [] : #si l'historique n'est pas vide, on l'affiche
		print("historique : \n")
		for i in range(len(historique)):
			print(i+1," : ",historique[i],"\n")
		print("Pour utiliser l'historique, veuillez entrer le numéro du mot.")
	print("Pour effectuer une recherche rapide entre deux mots, séparez les avec un '/' (mot1/mot2).")
	while(True):
		Linput = input("Mot : ")
		if historique != []: #si l'historique n'est pas vide
			if Linput in ["1","2","3","4","5"] and int(Linput) <= len(historique): #on vérifie si le choix est dans l'historique
				mot =  historique[int(Linput)-1]
				return mot
		if "/" in Linput: #on vérifie s'il souhaite effectuer la recherche rapide
			mot=Linput.split('/')
			if(isInDico("word", mot[0]) and isInDico("word", mot[1])): #on vérifie si les deux mots existent
				return Linput
			else:
				print("\nCes mots n'existent pas")
		else:
			if(isInDico("word", Linput)): #on vérifie si le mot existe
				return Linput
			else :
				print("\nL'entrée n'est pas valide ou ce mot n'existe pas")

"""
Objectif : Gère le choix du mode de l'utilisateur
Paramètres :
	-Entrée :
		-tabChoix : tableau contenant les différents choix possibles
	-Sortie : 
		le mode choisi
"""
def choixMode():
	print("\nSélectionner le type de recherche : ")
	print("\ta - recherche par lettre")
	print("\tz - recherche par phonèmes")
	print("\te - recherche complète")
	print("\tr - Retour au menu")
	while(True):
		selection=input("Choix du mode : ")
		if selection in ["a","z","e","r"]: #si le mode choisi est bien dans le tableau
			return selection
		else:
			print("\nL'entrée n'est pas valide, réessayez")
		

"""
Objectif : Gère la sélection de la longueur des syllabes par l'utilisateur
Paramètres :
	-Entrée :
		-message : message à afficher lors de la sélection
	-Sortie : 
		la longueur selectionnée
"""
def longueurSyllabe(message):
	x = True
	while x :
		l=input(message)
		if inputInt(l) :
			if int(l)>0: #on exige au moins 1
				x = False
		else:
			print("Vous n'avez pas entré un nombre convenable. Ressayer")
		
	return int(l)


"""
Objectif : Gère le mode personnalisée (lettre ou phonème)
Paramètres :
	-Entrée :
		-mode : mode sélectionné par l'utilisateur (word => lettren, phon => lettre)
		-mot : mot entré par l'utilisateur
		-langue : langue choisie par l'utilisateur
		-dicoDico : dictionnaire contenant les fichiers + config de l'application
	-Sortie : 
		un entier (0 => revenir au menu, 1 => revenir au début de l'aide)
"""
def modePersonnalisé(mode,mot,langue,dicoDico):
	x = longueurSyllabe("Longueur de la syllabe à enlever : ")
	y = longueurSyllabe("Longueur de la syllabe à ajouter : ")
	print("Recherche des contrepétries possibles ...")
	calculTempsExecution(len(mot),y,"seul")
	listeDeMotCop = aide(mot,x,y,mode,langue,dicoDico)

	if(len(listeDeMotCop) == 0 ):
		affichagePasResultat(mot,"",x,y,"","",dicoDico['config'],mode)
		return
	if(mode == "word"):
		affichageBase(mot,listeDeMotCop,x)
	else:
		affichageBase(Mot_to_Phon_Only(arbre_mot, mot),listeDeMotCop,x)
	if(mode == 'word'):
		message="effectuer la recherche avec les phonèmes"
	else:
		message="effectuer la recherche avec les lettres"
	selectMot = None
	boucle = True
	while(boucle):
		selectMot = input(f"\na - quitter l'aide, z - revenir au début de l'aide, e - {message} \nou numéro de l'échange qui vous intéresse : \n")
		if selectMot == "a":
			return 0
		elif selectMot == "z":
			return 1
		elif selectMot == "e":
			if mode == 'word' :
				mode = 'phon'
			else :
				mode = 'word'
			listeDeMotCop = aide(mot,x,y,mode,langue,dicoDico)
		elif inputInt(selectMot) :
			selectMot = int(selectMot)
			if selectMot <= len(listeDeMotCop) and selectMot > 0: #evite les erreurs de segmentations
				boucle = False
		else:
			print("\nL'entrée n'est pas valide, réessayez")

		print("Veuillez sélectionner la longueur des résultats souhaités")
		minimum=selectionLongueurMot("Longueur minimum (-1=toutes les longueurs) : ")
		maximum=selectionLongueurMot("Longueur maximum (-1=toutes les longueurs) : ")
		listeAffichage, compteur = aideRechDicoGeneral(mot,selectMot, listeDeMotCop,minimum,maximum,dicoDico,mode)

	# en cas de liste vide, affichant qu'aucune possibilité n'est trouvée
	if len(listeAffichage) >0:
		#if (diconfig["FiltreGrammatical"] == "Oui"):
		#	listeAffichage = gramFiltre(listeAffichage, mot,langue,mode)
		if(mode=='word'):
			return affiRechLettre(listeAffichage, compteur, mot)
		else:
			return affiRechSon(listeAffichage, compteur, mot,langue, dicoDico)
	else:
		if(mode=="word"):
			mot2=listeDeMotCop[selectMot-1][0]
		else:
			mot2=listeDeMotCop[selectMot-1][3]
		affichagePasResultat(mot,mot2,x,y,minimum,maximum,dicoDico['config'],mode)


"""
Objectif : Gère le mode plusieurs (lettre ou phonème)
Paramètres :
	-Entrée :
		-mot : mot entré par l'utilisateur
		-langue : langue choisie par l'utilisateur
		-dicoDico : dictionnaire contenant les fichiers + config de l'application
	-Sortie : 
		un entier (0 => revenir au menu, 1 => revenir au début de l'aide)
"""
def recherchePlusieurs(mot,langue,dicoDico):
	dicoResWord = {}
	dicoResPhon = {}
	longueurMot = len(mot)

	#Ce mode met les mots coupés et active par défaut le filtre grammatical
	oldMotCoupe=dicoDico['config']['MotCoupe']
	dicoDico['config']['MotCoupe']="Non"
	oldFiltreGram=dicoDico['config']['FiltreGrammatical']
	dicoDico['config']['FiltreGrammatical']="Oui"
	ecriturePhonMot = Mot_to_Phon_Only(arbre_mot, mot)

	calculTempsExecution(len(mot)-1,4,"plusieurs")
	for x in range(1,longueurMot): #pour chaque tranche possible du mot
		dicoResWord[f"{x}"]=[]
		dicoResPhon[f"{x}"]=[]
		for y in range(1,4): #pour chaque longueur d'échange possible
			listeRes = aide(mot,x,y,"word",langue,dicoDico)
			if(len(listeRes) != 0):
				dicoResWord[f"{x}"].extend(listeRes)
			listeRes = aide(mot,x,y,"phon",langue,dicoDico)
			if(len(listeRes) != 0):
				dicoResPhon[f"{x}"].extend(listeRes)
	boucle=True
	while(boucle):
		affichageBasePlusieurs(mot,dicoResWord,dicoResPhon)
		while(True):
			choix = input("\na -> Quitter l'aide, z -> Retour au menu, entrer le numéro des résultats à afficher : ")
			if(choix == "a"):
				return choix
			elif(choix == "z"):
				return 1
			elif inputInt(choix):
				choix=int(choix)
				if(choix < 0 or choix > (len(dicoResWord) + len(dicoResPhon))):
					print("Vous n'avez pas entrer un entier qui fonctionne. Ressayer.")
					continue
				elif(choix <= len(dicoResWord)):
					listeDeMotCop = dicoResWord[str(choix)]
					mode="word"
					break
				else:
					choix = abs(len(dicoResWord) - choix)
					listeDeMotCop = dicoResPhon[str(choix)]
					mode="phon"
					break	
		if(mode=='word'):
			affichageBase(mot,listeDeMotCop,choix)
		else:
			affichageBase(ecriturePhonMot,listeDeMotCop,choix)
		boucle2 = True
		while(boucle2):
			selectMot = input("\na -> Quitter l'aide, z -> Retour au menu, e -> Revenir à la sélection précédente,\n ou numéro de l'échange qui vous intéresse : \n")
			if selectMot == "a" or selectMot == "z":
				return selectMot
			elif selectMot == "e" : #evite les erreurs de segmentations
				boucle2 = False
			elif inputInt(selectMot) :
				selectMot = int(selectMot)
				if (selectMot <= len(listeDeMotCop) and selectMot > 0):
					boucle2 = False
			else:
				print("\nL'entrée n'est pas valide, réessayez")

		if(selectMot == "e"):
			continue
		listeAffichage, compteur = aideRechDicoGeneral(mot,selectMot, listeDeMotCop,-1,-1,dicoDico,mode)

		# en cas de liste vide, affichant qu'aucune possibilité n'est trouvée
		if len(listeAffichage) >0:
			if(mode=='word'):
				continuer = affiRechLettre(listeAffichage, compteur, mot)
			else:
				continuer = affiRechSon(listeAffichage, compteur, mot,langue, dicoDico)
			if continuer == 0 or continuer == -1:
				return abs(continuer)
		else:
			if(mode=="word"):
				mot2=listeDeMotCop[selectMot-1][0]
			else:
				mot2=listeDeMotCop[selectMot-1][3]
			affichagePasResultat(mot,mot2,x,y,-1,-1,dicoDico['config'],mode)
	#faire la recherche des quadruplé
	dicoDico['config']['MotCoupe']=oldMotCoupe
	dicoDico['config']['FiltreGrammatical']=oldFiltreGram


def affichagePasResultat(mot,mot2,x,y,minimum,maximum,diconfig,mode):
	message="Aucune correspondance n'a été trouvée\n"
	if(mode=="phon"):
		message1="phonème(s)"
	else:
		message1="lettre(s)"
	message+=f"Voici les options sélectionnées : \n\t-Recherche au sein du mot : {mot} en échangeant des {message1}"
	if mot2 != "":
		message+=f"\n\t-Echange de {x} {message1} par {y} {message1}"
		message+=f"\n\t-Recherche de quadruplé entre {mot} et {mot2}"
		if(minimum == -1):
			message+="\n\t-Longueur minimum des résultats : aucune"
		else:
			message+=f"\n\t-Longueur minimum des résultats : {minimum}"
		if(maximum == -1):
			message+="\n\t-Longueur maximum des résultats : aucune"
		else:
			message+=f"\n\t-Longueur maximum des résultats : {maximum}"

	if(len(diconfig['Themes'])==0):
		message+="\n\t-Aucun thème d'appliqué"
	else:
		message+="\n\t-Thème(s) appliqué(s) : "
		for theme in diconfig['Themes']:
			message += theme + ", "
	message+=f"\n\t-Filtre grammatical : {diconfig['FiltreGrammatical']}\n"
	print(message)
	input('Tapez sur une touche pour revenir en avant')