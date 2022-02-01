import language_tool_python
import json
import os
import collections

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
def configFiltre(tabDicoThemeDispo):
	with open('data/config.json','r') as diconfig_:
		diconfig = json.load(diconfig_)
		n = selectionChoix("\nActiver filtre Grammaticale\n(1:Oui/0:Non/autre:defaut):")
		if n == 1:
			diconfig["FiltreGrammatical"] = "Oui"
		elif n == 0:
			diconfig["FiltreGrammatical"] = "Non"

		diconfig["Themes"]=changerDicoTheme(tabDicoThemeDispo)
		n = selectionChoix("\nActiver effaçage définitif (empêche de voir les saisies précédantes)\n(1:Oui/0:Non/autre:defaut):")
		if n == 1:
			diconfig["EffacerComplétement"] = "Oui"
		elif n == 0:
			diconfig["EffacerComplétement"] = "Non"
	print("\n")
	for i in diconfig.keys():
		print(f"{i}  -  {diconfig[i]}")
	with open('data/config.json','w') as diconfig_:
		json.dump(diconfig,diconfig_) #écrit dans le fichier

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
	for theme in tabDicoThemeDispo:
		choix=selectionChoix(f"Appliquer le thème {theme} ? (1=oui/0=non) :") #gère ce qui est entré
		if(choix == 1): #s'il a sélectionné le thème
			tabChoix.append(theme) #on l'ajoute dans les réponses
	return tabChoix


"""
Objectif : Renvoie le choix entré par l'utilisateur
Paramètres :
	-Entrée :
		-message : Message à afficher
	-Sortie : 
		un entier
"""
def selectionChoix(message):
	while(True):
		try:
			entier=int(input(message))
			if(entier == 0 or entier==1):
				print(entier)
				return entier
		except:
			print("Vous n'avez pas entré un entier. Réessayer")
			entier=input(message)
		print("Vous n'avez pas entré un entier convenable. Ressayer")


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
			try:
				n = int(input("\nEntré le numéro de la langue voulue : "))
				if n in range(len(tabLanguesDispo)+1) and n>0: #on s'assure qu'il sélectionne une langue qui existe
					diconfig['langue']=tabLanguesDispo[n-1]
					break
				print("Numéro de langue incorrect")
			except:
				print("Vous n'avez pas entré un entier. Réessayer")
	with open("data/config.json","w") as file:
		json.dump(diconfig,file) #on écrit dans le fichier
		



#-------------------------------------------------------------------------------


"""
Applique les filtres et affiche les résultats en fonctions de la config
donnée par l'utilisateur
"""
def affiRechFiltre(nvDico,mode):

	with open('data/config.json') as diconfig_:
		diconfig = json.load(diconfig_)

	print('\nTraitement en cours ...')
	diconfig = changerfiltre(diconfig)


	if mode == 'phon':
		if diconfig["FiltreGrossier"] == "Oui":
			nvDico = filtreMix(nvDico) #On filtre en ne gardant que ce qui est grossier
		count1 = 0
		count2 = 0
		for key in nvDico:
			count1 += len(nvDico[key])

		StockPourkey = ""
		compteur = -1
		dicores = []

		for key in nvDico:

			if diconfig["FiltreGrammatical"] == "Oui":

				for j in nvDico[key]:
					j = ' '.join(j) #Joint chaque élément par "" de nvDico[key]
					if j[0] == " ":
						j = j[1:] #Si la phrase commence par un espace, on l'enlève
					j = j.capitalize() #Met la première en majuscule et toutes les autres en minuscules
					compteur += 1

					if StockPourkey != key and len(language_tool_python.LanguageToolPublicAPI('fr').check(j)) == 0:
						print(compteur, " -->", j)
						StockPourkey = key
						dicores.append(key)
					else:
						compteur -= 1

			else:
				for j in nvDico[key]:
					j = ' '.join(j)
					if j[0] == " ":
						j = j[1:]
					j = j.capitalize()
					compteur += 1
					if StockPourkey != key:
						print(compteur, " -->", j)
						StockPourkey = key
						dicores.append(key)
					else:
						compteur -= 1

		choixutilisateur = 1
		while choixutilisateur in range(compteur):
			try:
				choixutilisateur = int(input(
				"\n-1 : quitter/ -2 revenir au menu principal ou \nChiffre pour ortographe\n"))
			except:
				print("\nVous n'avez pas saisi un chiffre")
				continue
			if (choixutilisateur) <= compteur and choixutilisateur > -1:
				for j in nvDico[dicores[choixutilisateur]]:
					j = ' '.join(j)
					if j[0] == " ":
						j = j[1:]
					j = j.capitalize()
					if diconfig["FiltreGrammatical"] == "Oui":
						matches = language_tool_python.LanguageToolPublicAPI('fr').check(j)
						if len(matches) == 0:
							print(j)
					else:
						print(j)

			elif choixutilisateur == -1:
				return 0
			elif choixutilisateur == -2:
				return 1
			else:
				print("Pas de résultat")

	if mode == 'word':
		#attention, ici nvDico est une liste de tuple, plus un dico
		#filtrage par grammaire de la phrase
		nvListe = [nvDico[0]]
		if diconfig["FiltreGrossier"] == "Non" and diconfig["FiltreGrammatical"] == "Non":
			for i in nvDico[1:]: #On renvoie les résultats qu'on avaient de base
				nvListe.append(" ".join(i[0]))
			return nvListe

		with open('data/DicoVulgaire.json') as vulgaire:
			BDvulgaire = json.load(vulgaire)

		if diconfig["FiltreGrammatical"] == "Oui":
			for contrepet in nvDico[1:]:
				str = " ".join(contrepet[0])
				j = str.capitalize()

				if len(language_tool_python.LanguageToolPublicAPI('fr').check(j)) == 0:
					nvListe.append(contrepet)

		tmpListe = []
		if diconfig["FiltreGrammatical"] == "Oui":
			tmpListe = nvListe[:]
			nvListe = [nvListe[0]]
		else:
			tmpListe =  nvDico[:]
		#filtrage par mot vulgaires
		for contrepet in tmpListe[1:]:
			if diconfig["FiltreGrossier"] == "Oui":
				test = False
				for i in contrepet[0]:
					if i in BDvulgaire:
						test = True
						break
				if test:
					nvListe.append(" ".join(contrepet[0]))
			else :
				nvListe.append(" ".join(contrepet[0]))
		return nvListe


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
def GramFiltre(listeOrigine, mot_origine,langue,mode):
	nouvelleListe = []
	with open(f'data/{langue}/dicoClassGramm{langue.capitalize()}.json') as tmp:
			dicoClassGramm = json.load(tmp)
	#arbre_mot = arbre qui contient tous les mots
	for pack in listeOrigine:
		#On récupère les classes grammaticales des réponses
		if(mode == "word"):
			classGramMot1 = dicoClassGramm[mot_origine]
			classGramMot2 = dicoClassGramm[pack[4]]
			classGramMot3 = dicoClassGramm[pack[2]]
			classGramMot4 = dicoClassGramm[pack[3]]
		if(mode == "phon"):
			with open(f'data/{langue}/dicoPhoncom{langue.capitalize()}.json') as tmp:
				dicoPhon = json.load(tmp)
			classGramMot1 = dicoClassGramm[mot_origine]
			classGramMot2 = dicoClassGramm[dicoPhon[pack[4]][0]]
			classGramMot3 = dicoClassGramm[dicoPhon[pack[2]][0]]
			classGramMot4 = dicoClassGramm[dicoPhon[pack[3]][0]]
		for i in range(len(classGramMot1)): #On parcours les classes grammaticales du mot entré par l'utilisateur
			if(classGramMot1[i] in classGramMot2 and classGramMot1[i] in classGramMot3 and classGramMot1[i] in classGramMot4): #s'ils ont la même classe grammaticale
					nouvelleListe.append(pack) #on l'ajoute aux réponses
	return nouvelleListe

"""
Renvoie True si le mot est dans au moins un des dico de listeDico
Paramètre :
	-Entrée :
		-mot : mot à vérifier
		-listeDico : tableau contenant les dico par thèmes sélectionnés par l'utilisateur
	-Sortie :
		-un boolean
"""
def filtreTheme(mot,listeDico):
	boolean=False
	if(len(listeDico)==0):
		return True
	for dico in listeDico:
		if(mot in dico):
			boolean=True
			break
	return boolean
