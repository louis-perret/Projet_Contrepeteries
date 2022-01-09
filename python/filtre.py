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
def configFiltre():
	with open('data/config.json','r') as diconfig_:
		diconfig = json.load(diconfig_)
		n = input("\nActiver filtre Grammaticale\n(1:Oui/0:Non/autre:defaut):")
		if n == '1':
			diconfig["FiltreGrammatical"] = "Oui"
		elif n == '0':
			diconfig["FiltreGrammatical"] = "Non"

		n = input("\nActiver filtre Grossier\n(1:Oui/0:Non/autre:defaut):")
		if n == '1':
			diconfig["FiltreGrossier"] = "Oui"
		elif n == '0':
			diconfig["FiltreGrossier"] = "Non"

		n = input("\nActiver effaçage définitif (empêche de voir les saisies précèdantes)\n(1:Oui/0:Non/autre:defaut):")
		if n == '1':
			diconfig["EffacerComplétement"] = "Oui"
		elif n == '0':
			diconfig["EffacerComplétement"] = "Non"
	print("\n")
	for i in diconfig.keys():
		print(f"{i}  -  {diconfig[i]}")
	with open('data/config.json','w') as diconfig_:
		json.dump(diconfig,diconfig_) #écrit dans le fichier

#-------------------------------------------------------------------------------

"""
Objectif : Met à jour les filtres
Paramètres :
	-Entrée :
		-diconfig : dictionnaire qui contient la configuration
	-Sortie : 
		-diconfig : dictionnaire qui contient la configuration
"""
def changerfiltre(diconfig):
	n = input("\nActiver filtre Grammaticale\n(1:Oui/0:Non/n'importe quelle clef:défaut):")
	if n == '1':
		diconfig["FiltreGrammatical"] = "Oui"
	elif n == '0':
		diconfig["FiltreGrammatical"] = "Non"

	n = input("\nActiver filtre Grossier\n(1:Oui/0:Non/n'importe quelle clef:défaut):")
	if n == '1':
		diconfig["FiltreGrossier"] = "Oui"
	elif n == '0':
		diconfig["FiltreGrossier"] = "Non"

	print("\n")
	return diconfig
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
			print(f"-{tabLanguesDispo[i]}\n")
		n = input()
		while(n not in tabLanguesDispo): #on s'assure qu'il sélectionne une langue qui existe
			n = input("\nChoisissez la langue :\n")
		diconfig['langue']=n
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
