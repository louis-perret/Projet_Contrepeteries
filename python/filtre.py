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
"""
Modifie le fichier de configuration des filtres.
"""
def configFiltre(tabDicoThemeDispo,dicoDico):
	with open('data/config.json','r') as diconfig_:
		diconfig = json.load(diconfig_)
		n = selectionChoix("\nActiver filtre Grammaticale\n(a:Oui/z:Non/autre:defaut):")
		if n == "a":
			diconfig["FiltreGrammatical"] = "Oui"
		elif n == "z":
			diconfig["FiltreGrammatical"] = "Non"

		diconfig["Themes"]=changerDicoTheme(tabDicoThemeDispo)

		n = selectionChoix("\nActiver les mots coupés\n(a:Oui/z:Non/autre:defaut):")
		if n == "a":
			diconfig["MotCoupe"] = "Oui"
		elif n == "z":
			diconfig["MotCoupe"] = "Non"

		n = selectionChoix("\nActiver effaçage définitif (empêche de voir les saisies précédantes)\n(a:Oui/z:Non/autre:defaut):")
		if n == "a":
			diconfig["EffacerComplétement"] = "Oui"
		elif n == "z":
			diconfig["EffacerComplétement"] = "Non"
	print("\n")
	for i in diconfig.keys():
		print(f"{i}  -  {diconfig[i]}")
	with open('data/config.json','w') as diconfig_:
		json.dump(diconfig,diconfig_) #écrit dans le fichier

	listeDicoTheme=[]
	for theme in diconfig['Themes']:
		if('Non' in theme): #pour éviter les problèmes de fichier qui n'existent pas
			theme=theme.replace("Non-","")
		with open(f'data/{dicoDico["config"]["langue"]}/dico{theme}{dicoDico["config"]["langue"].capitalize()}.json') as dicoTheme:
			listeDicoTheme.append(json.load(dicoTheme))
	dicoDico['Themes']=listeDicoTheme
	dicoDico['Config']=diconfig
#-------------------------------------------------------------------------------

"""
Objectif : Met à jour les thèmes choisis par l'utilisateur
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
		if(choix == 1): #si le thème possèdait un inverse (vulgaire -> non vulgaire par exemple)
			choix=0 #on repasse le choix à 0
			continue #et on saute le thème d'après qui est son inverse
		choix=selectionChoix(f"Appliquer le thème {theme} ? (a=oui/z=non) :") #gère ce qui est entré
		if(choix == "a"): #s'il a sélectionné le thème
			tabChoix.append(theme) #on l'ajoute dans les réponses
		if("Non" in theme): #et si le thème était un thème inverse
			choix="z" #on repasse le choix à 0 pour éviter de sauter celui d'après qui n'est pas un inverse
	return tabChoix


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
		entier=input(message)
		if(entier == "a" or entier=="z"):
			print(entier)
			return entier
		print("Vous n'avez pas entré une lettre convenable. Ressayer")


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
	for classGram in classGramMotOrigine:
		if(classGram in classGramMot2): #si ils ont au moins une classe grammticale en commun
			return True #on renvoie true
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
