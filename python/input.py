from filtre import * #Importe toutes les fonctions du fichier filtre
import sys #Importe fonctions système

dicoDispo={"fr": ["Vulgaire","Non-Vulgaire","Informatique",],"en": []} #initialise les langues disponibles ainsi que ls thèmes disponibles pour chaque langue
configLangue(list(dicoDispo.keys())) #on met à jour la langue choisie
print("Chargement des dictionnaires")
from arbin import * #on charge le dico
with open("data/config.json","r") as file:	
	diconfig = json.load(file) #on charge le fichier

langue=diconfig['langue']
dicoDico={}
dicoDico["config"]=diconfig
listeDicoTheme=[]
if(dicoDispo[langue] != []): #si la langue choisie dispose de dico par thème
	for theme in diconfig['Themes']: #on les charge un à un
		if('Non' in theme): #pour éviter les problèmes de fichier qui n'existent pas
			theme=theme.replace("Non-","")
		with open(f'data/{langue}/dico{theme}{langue.capitalize()}.json') as dicoTheme:
			listeDicoTheme.append(json.load(dicoTheme))

dicoDico['Themes']=listeDicoTheme
with open(f"data/{langue}/dicoPhoncom{langue.capitalize()}.json") as Phon :
	dicoPhon = json.load(Phon)
	dicoDico['DicoPhon']=dicoPhon

with open(f'data/{langue}/dicoClassGramm{langue.capitalize()}.json') as tmp:
			dicoClassGramm = json.load(tmp)
			dicoDico['DicoGram']=dicoClassGramm

boucle = True
memoireImport = set()
historique = []
# boucle pour recommencer le programme
while boucle:
	clear()
	valide = True
	test = True
	n = 0
	# selecteur type de programme:
	print(
"""\nSelectionnez le mode que vous souhaitez : \n
a. Recherche de contrepèteries dans un mot
z. Recherche de contrepèteries dans une phrase
e. Configuration des filtres
r. Quitter\n""")
	while test:
		try:
			n = input() #Récupère ce que rentre l'utilisateur
			if n == "r":
				sys.exit()
			elif n in ["a","z","e"]: #de 1 à 4 exclu
				test = False
			else:
				print("Votre saisie n'est pas valide\n")
		except ValueError:
			print("Vous n'avez pas saisie un caractère valide.\n")

		
# ------------------------------------------------------------------------------
	if n == "e":
		configFiltre(dicoDispo[diconfig['langue']],dicoDico)
# ------------------------------------------------------------------------------
	# aide à contrepeterie
	elif n == "a":
		if 'aide' not in memoireImport:
			from menuAideContre import *
		memoireImport.add('aide')
		clear()
		historique = aideContrepetrie(dicoDico,historique)

# ------------------------------------------------------------------------------
	# recherche de contrepeterie
	elif n == "z":
		if 'rech' not in memoireImport:
			from menuAidePhrase import *
		memoireImport.add('rech')

		with open('data/config.json','r') as diconfig_:
			langue=dicoConfig['langue'] #on récupère la langue entrée par l'utilisateur
		
		test = aideContrepetriePhrase(dicoDico,langue)
		if test == 0:
			sys.exit()
		elif test == 1:
			continue
# ------------------------------------------------------------------------------

	# boucle demande de fin de programme
	tmp = None
	test2 = True
	passeur = 1
	while passeur != 0:
		try:
			tmp = input("a : Quitter l'application / z : Retour au début ")
			passeur = 0
		except ValueError:
			print("Entrée invalid veuillez réessayer.\n")
		if tmp == "a":
			test2 = False
			boucle = False

		elif tmp == "z":
			test2 = False
			clear()
