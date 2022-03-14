import language_tool_python
import json
import os
import collections
from utilitaires import *
"""
Efface le terminal ou met une série de \n pour simuler un éffacement du terminal
selon fichier config.json
"""

def clear():
	with open('data/config.json','r') as diconfig_: #lit le fichier et met dans diconfig_
		diconfig = json.load(diconfig_) #charge le fichier dans un dico

		if diconfig["EffacerComplétement"] == "Oui":
			os.system('clear') if os.name == 'posix' else os.system('clear') #opérateur ternaire : value_if if condition else value_else
		else :
			print("\n"*60)
#-------------------------------------------------------------------------------

def explicationFiltre():
	print("Explication des différents filtres disponibles : \n")
	print("\t-Filtre grammaticale : Permet de filtrer les résultats suivant leur classe grammaticale.\n\tIl y a deux filtres grammaticales disponibles :\n\t\t 1.Garde les résultats qui possède au moins une classe grammaticale en commun\n\t\t 2.Sélectionner une classe grammaticale en particulier et garde les résultats qui possède cette classe.")
	print("\t Pour sélectionner un des deux filtres grammaticales, activer le filtre grammaticale pour pouvoir choisir l'un des deux.")
	print("\n\t-Filtre par thème : Sélection de thèmes disponibles. Garde les résultats qui appartiennent à au moins un des thèmes sélectionnés.")
	print("\n\t-Mot coupé : Permet d'activer la rechercher des mots coupés et des regroupement (seulement dans les phrases) de mots dans les recherches.")
	print("\n\t-EffacerComplétement : Permet d'effectuer un clear() du terminal à chaque navigation au sein de l'application.")
	print("\n")

	print("Exemple d'utilisation des filtres :")
	print("Premier filtre grammaticale : je recherche dans le mot 'code' -> mes résultats seront soit des noms soit des verbes")
	print("Deuxième filtre grammaticale : je sélectionne 'verbe' comme classe grammaticale, je recherche dans 'code' -> j'aurais que des verbes comme résultats")
	print("Filtre par thème : Si je sélectionne le thème Vulgaire et Informatique, je recherche dans code -> j'aurais soit des résultats soit grossiés, soit en rapport avec l'informatique")
	print("\n")
"""
Objectif : Change une partie/toute la configuration de l'utilisateur
Paramètres :
	-Entrée :
		-tabDicoThemeDispo : thèmes disponibles dans l'applications
		-dicoDico : dictionnaire contenant les fichiers de l'application et la configuration de l'utilisateur
		-diconfig : dictionnaire de la configuration
	-Sortie : 
		aucun
"""
def configFiltre(tabDicoThemeDispo,dicoDico):
	diconfig = dicoDico['config']
	boucle=True
	explicationFiltre()
	while(boucle):
		print("Voici votre configuration actuelle :")
		j=0
		for i in diconfig.keys():
			if(i != "langue"):
				print(f"\t {j} {i}  -  {diconfig[i]}")
				j=j+1
		boucle2=True
		while(boucle2):
			choix = input("a: Retour au menu \nEntrer le numéro de la configuration à changer :\n")
			if(choix == "a"):
				boucle2=False
				boucle=False
				continue
			elif(inputInt(choix)):
				choix=int(choix)
				if(choix >= 0 and choix < j):
					boucle2=False
					continue
			print("Vous n'avez pas entré un choix correcte. Réessayer. ")

		if(choix==0):
			diconfig["FiltreGrammatical"] = choixFiltreGrammatical(dicoDico["config"]["langue"])
		elif(choix==1):
			diconfig["Themes"]=changerDicoTheme(tabDicoThemeDispo)
		elif(choix==2):
			diconfig["MotCoupe"] = selectionChoix("\nActiver les mots coupés\n(a:Oui/z:Non/autre:defaut):")
		elif(choix==3):
			diconfig["EffacerComplétement"] = selectionChoix("\nActiver effaçage définitif (empêche de voir les saisies précédantes)\n(a:Oui/z:Non/autre:defaut):")

	"""
	print("\nVoici votre nouvelle configuration : ")
	for i in diconfig.keys():
		print(f"{i}  -  {diconfig[i]}")
	"""
	with open('data/config.json','w') as diconfig_:
		json.dump(diconfig,diconfig_) #écrit dans le fichier

	listeDicoTheme=[]
	for theme in diconfig['Themes']:
		if('Non' in theme): #pour éviter les problèmes de fichier qui n'existent pas
			theme=theme.replace("Non-","")
		with open(f'data/{dicoDico["config"]["langue"]}/dico{theme}{dicoDico["config"]["langue"].capitalize()}.json') as dicoTheme:
			listeDicoTheme.append(json.load(dicoTheme))
	dicoDico['Themes']=listeDicoTheme
	dicoDico['config']=diconfig


"""
Objectif : Met à jour les thèmes choisi par l'utilisateur
Paramètres :
	-Entrée :
		-tabDicoThemeDispo : thèmes disponibles dans l'applications
	-Sortie : 
		-un tableau contenant les thèmes sélectionnés
"""
def changerDicoTheme(tabDicoThemeDispo):
	tabChoix=[] #contiendra les choix de l'utilisateurs
	if(len(tabDicoThemeDispo) == 0):
		print("Aucun thème pour cette langue")
		return list()
	choix=0
	for theme in tabDicoThemeDispo:
		if(choix == "Oui"): #si le thème possèdait un inverse (vulgaire -> non vulgaire par exemple)
			choix=0 #on repasse le choix à 0
			continue #et on saute le thème d'après qui est son inverse
		choix=selectionChoix(f"Gardez que les mots {theme} ? (a=oui/z=non) :") #gère ce qui est entré
		if(choix == "Oui"): #s'il a sélectionné le thème
			tabChoix.append(theme) #on l'ajoute dans les réponses
		if("Non" in theme): #et si le thème était un thème inverse
			choix=0 #on repasse le choix à 0 pour éviter de sauter celui d'après qui n'est pas un inverse
	return tabChoix


"""
Objectif : Met à jour le filtre grammatical choisi par l'utilisateur
Paramètres :
	-Entrée :
		-langue : langue choisie par l'utilisateur
	-Sortie : 
		-string : choix de l'utilisateur
"""
def choixFiltreGrammatical(langue):
	n = selectionChoix("\nActiver filtre Grammaticale\n(a:Oui/z:Non/autre:defaut):")
	if n == "a":
		n=selectionChoix("\na:Garder les résultats de mêmes classes grammaticales,ou\nz:Sélectionner une classe grammaticale en particulier : ")
		if(n=="a"):
			return n
		else:
			n=selectionClasseGrammaticale(langue)
			return n
	return n

"""
Objectif : Renvoie le choix entré par l'utilisateur pour les
Paramètres :
	-Entrée :
		-message : Message à afficher
	-Sortie : 
		un entier
"""
def selectionChoix(message):
	while(True):
		choix=input(message)
		if(choix == "a"):
			return "Oui"
		elif(choix == "z"):
			return "Non"
		print("Vous n'avez pas entré une lettre convenable. Réessayer")

"""
Objectif : Permet de choisir une classe grammaticale en particulier
Paramètres :
	-Entrée :
		-langue : langue choisie par l'utilisateur
	-Sortie : 
		-string : classe grammaticale choisie par l'utilisateur
"""
def selectionClasseGrammaticale(langue):
	if langue == 'fr':
		tabClasseGrammaticale=['nom','verbe','adjectif','adverbe','proposition','pronom','nom propre']
	elif langue == 'en':
		tabClasseGrammaticale=['noun','verb','adjective','adverb','preposition','pronoun','proper noun']
	for i in range(len(tabClasseGrammaticale)):
		print(f"{i} - {tabClasseGrammaticale[i]}")

	boucle=True
	while(boucle):
		choix=input("Sélectionnez la classe grammaticale que vous souhaitez garder (à l'aide de son indice) : ")
		if(inputInt(choix)):
			choix=int(choix)
			if(choix >= 0 and choix < len(tabClasseGrammaticale)):
				print(choix)
				print(tabClasseGrammaticale)
				print(tabClasseGrammaticale[choix])
				return tabClasseGrammaticale[choix]

#-------------------------------------------------------------------------------


"""
Objectif : Met à jour la langue sélectionné
Paramètres :
	-Entrée :
		-tabLanguesDispo : tableau contenant les langues supportées par l'application
	-Sortie : 
		aucun
"""
def configLangue(tabLanguesDispo):
	with open("data/config.json","r") as file:	
		diconfig = json.load(file) #on charge le fichier

		print("\nChoisissez la langue :\n")
		for i in range(len(tabLanguesDispo)):
			print(f"{i+1} - {tabLanguesDispo[i]}\n")
		while(True):
			n = input("\nEntré le numéro de la langue voulue : ")
			if inputInt(n) :
				n = int(n)
				if n in range(len(tabLanguesDispo)+1) and n>0: #on s'assure qu'il sélectionne une langue qui existe
					diconfig['langue']=tabLanguesDispo[n-1]
					break
			print("Numéro de langue incorrect")
	with open("data/config.json","w") as file:
		json.dump(diconfig,file) #on écrit dans le fichier

# -------------------------------------------------------------------------------
"""
Filtre depuis un dictionnaire de phrase, garde toutes les phrases contenant
au moins un mot vulgaire.
"""
def filtreMix(dicoResult):

	with open('data/DicoVulgaire.json') as vulgaire:
		BDvulgaire = json.load(vulgaire) #dico contenant tous les mots vulgaires

	dicoFiltre = {} #nos mots filtrés à la fin
	for key in dicoResult:
		tmpListe = []

		dicoTmp = dicoResult[key] #on récupère les valeurs de chaque clé de dicoResult
		for i in range(len(dicoTmp)):
			test1 = False

			for value in dicoTmp[i]:
				# test si le contrepet contient un mot vulgaire
				if value in BDvulgaire:
					test1 = True
					break

			if test1:
				tmpListe.append(dicoTmp[i])

		if tmpListe != []:
			dicoFiltre[key] = tmpListe

	return dicoFiltre

#-------------------------------------------------------------------------------
"""
Objectif : Définit le filtre grammatical (aide à la contrepèterie)
Paramètres : 
	-Entrée :
		listeOrigine : liste des résultats à traiter
		mot_origine : mot entré par l'utilisateur
	-Sortie :
		liste de quadruplets dont tous les élèments sont de la même classe Grammaticale
"""
def gramFiltre(classGramMotOrigine, mot2, mode, dicoGram, dicoPhon, diconfig):
	if(diconfig["FiltreGrammatical"] == "Non"): #si filtre pas activé
		return True #on renvoie true par défaut
	if(mode == "phon"): #si le mode est phonétique -> mot2 est en écriture phonétique
		mot2=dicoPhon[mot2][0] #on récupère son orthographe pour pouvoir ensuite récupérer correctement ses classes grammaticales

	classGramMot2 = dicoGram[mot2]

	if(diconfig["FiltreGrammatical"] == "Oui"):
		for classGram in classGramMotOrigine:
			if(classGram in classGramMot2): #s'ils ont au moins une classe grammticale en commun
				return True #on renvoie true
		return False
	else:
		if(diconfig["FiltreGrammatical"] in classGramMot2): #si mot2 a pour classe grammaticale celle sélectionnée par l'utilisateur
			return True
		return False

"""
Objectif : Renvoie True si le mot est dans au moins un des dico de listeDico
Paramètre :
	-Entrée :
		-mot : mot à vérifier
		-listeDico : tableau contenant les dico par thèmes sélectionnés par l'utilisateur
	-Sortie :
		-un boolean
"""
def filtreTheme(mot,listeDico, listeTheme):
	boolean=False
	if(len(listeDico)==0): #si aucun thème n'a été choisi
		return True #true par défaut
	i=0
	for dico in listeDico:
		if("Non" in listeTheme[0]):
			if(mot not in dico):
				boolean = True
				break
		else:
			if(mot in dico): #si le mot correspond à au moins un des thèmes
				boolean=True #on renvoie true
				break
	return boolean
