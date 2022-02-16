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
	tabMode=["Recherche personnalisée pour les lettres","Recherche personnalisée pour les phonèmes","Plusieurs lettres","Plusieurs sons"]
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
		choix=choixMode(tabMode) #sélection du mode

		clear()
		if(choix == 0 ):
			continuer=0
			continue

		elif choix == 1: #recherche personnalisée pour les lettres
			continuer=modePersonnalisé("word",mot,langue,dicoDico)

		elif choix == 2: #recherche personnalisée pour les sons
			continuer=modePersonnalisé("phon",mot,langue,dicoDico)

		elif choix == 3: #'nimporte quel nombre de lettre
			continuer=modePlusieurs("word",mot,langue,dicoDico)

		elif choix == 4: #n'importe quel nombre de phonèmes
			continuer=modePlusieurs("phon",mot,langue,dicoDico)

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
def choixMode(tabChoix):
	print("\nSélectionner le type de recherche : ")
	for i in range(len(tabChoix)):
		print(f"\t{i+1} - {tabChoix[i]}") #affiche les modes disponibles
	print("\t0 - Retour au menu")
	while(True):
		selection=inputInt("Choix du mode : ")
		if selection in range(len(tabChoix)+1): #si le mode choisi est bien dans le tableau
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
	l=inputInt(message)
	while(l<0): #on exige au moins 1
		print("Vous n'avez pas entré un nombre convenable. Ressayer")
		l=inputInt(message)
	return l


"""
Objectif : Gère le mode personnalisée (lettre ou phonème)
Paramètres :
	-Entrée :
		-dico : mode sélectionné par l'utilisateur (word => lettren, phon => lettre)
		-mot : mot entré par l'utilisateur
		-langue : langue choisie par l'utilisateur
		-diconfig : dictionnaire de configuration
	-Sortie : 
		un entier (0 => revenir au menu, 1 => revenir au début de l'aide)
"""
def modePersonnalisé(mode,mot,langue,dicoDico):
	x = longueurSyllabe("Longueur de la syllabe à enlever : ")
	y = longueurSyllabe("Longueur de la syllabe à ajouter : ")
	print("Recherche des contrepétries possibles ...")
	listeDeMotCop = aide(mot,x,y,mode,langue,dicoDico)

	if(len(listeDeMotCop) == 0 ):
		affichagePasResultat(mot,"",x,y,"","",dicoDico['config'],mode)
		return
	if(mode == 'word'):
		message="effectuer la recherche avec les phonèmes"
	else:
		message="effectuer la recherche avec les lettres"
	selectMot = None
	boucle = True
	while(boucle):
		selectMot = inputInt(f"\n0 = quitter l'aide,-1 revenir au début de l'aide, -2 {message} \nou numéro de l'échange qui vous intéresse : \n")
		if selectMot == 0:
			return 0
		elif selectMot == -1:
			return 1
		elif selectMot == -2:
			if mode == 'word' :
				mode = 'phon'
			else :
				mode = 'word'
			listeDeMotCop = aide(mot,x,y,mode,langue,dicoDico)
		elif selectMot <= len(listeDeMotCop) and selectMot > 0: #evite les erreurs de segmentations
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
		-mode: mode sélectionné par l'utilisateur (word => lettren, phon => lettre)
		-mot : mot entré par l'utilisateur
		-langue : langue choisie par l'utilisateur
	-Sortie : 
		un entier (0 => revenir au menu, 1 => revenir au début de l'aide)
"""
def modePlusieurs(mode,mot,langue,dicoDico):
	print("Recherche des échanges possibles sur les différentes tranches :")
	print("\nChargement en cours...\n")

	if(mode=="word"):
		sliceCorr = aideSyllSubs(mot) #récupère le dico qui a pour clé les lettres à changer et comme valeur tous les mots obtenus
	if(mode=="phon"):
		sliceCorr = aideMultiSonSubs(mot) #récupère le dico qui a pour clé les lettres à changer et comme valeur tous les mots obtenus
	# si les tranches n'avait pas de correspondance:
	if isinstance(sliceCorr, bool):
		clear()
		print("Ce mot n'est pas dans notre lexique, nous ne pouvons pas trouver son phonème.\n")
		return 1
	else:
		while(True):
			if(mode=="word"):
				syllOrigine = affiNbCorrTranche(sliceCorr)
			if(mode=="phon"):
				syllOrigine = affiNbCorrTranche2(sliceCorr)
			if syllOrigine == 0:
				return 0
			elif syllOrigine == -1:
				clear()
				return 1

			if(mode=="word"):
				selectMot = affiPageParPage(sliceCorr[syllOrigine], syllOrigine, mot)
			if(mode=="phon"):
				selectMot = affiPageParPage2(sliceCorr[syllOrigine], syllOrigine, mot)
			if selectMot == 0:
				return 0
			elif selectMot == -1:
				return 1
			elif isinstance(selectMot, str):
				break


		if(mode=="word"):
			(listeAffichage, compteur, diconfig) = aideSyllRechDico(mot, selectMot, syllOrigine)
		if(mode=="phon"):
			(listeAffichage, compteur, diconfig) = aideMultiSonRechDico(mot, selectMot, syllOrigine)
		if (diconfig["FiltreGrammatical"] == "Oui"):
			listeAffichage = GramFiltre(listeAffichage, mot,langue,mode)

		if(mode=="word"):
			return affiRechLettre(listeAffichage, compteur, mot)
		if(mode=="phon"):
			return affiRechSon(listeAffichage, compteur, mot,langue)



def affichagePasResultat(mot,mot2,x,y,minimum,maximum,diconfig,mode):
	message="Aucune correspondance n'a été trouvée\n"
	if(mode=="phon"):
		message1="phonème(s)"
	else:
		message1="lettre(s)"
	message+=f"Voici les options sélectionnées : \n\t-Recherche au sein du mot : {mot} en échangeant des {message1}"
	if mot2 != "":
		message+="f\n\t-Echange de {x} {message1} par {y} {message1}"
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