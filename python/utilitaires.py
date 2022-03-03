import string

"""
Objectif : Renvoie la longueur sélectionner par l'utilisateur
Paramètres :
	-Entrée :
		-message : Message à afficher
	-Sortie : 
		un entier
"""
def selectionLongueurMot(message):
	l=input(message)
	while(not inputInt(l)):
		print("Vous n'avez pas entré un entier convenable. Ressayer")
		l=inputInt(message)
	return int(l)


"""
Objectif : Renvoie la longueur sélectionner par l'utilisateur
Paramètres :
	-Entrée :
		-message : Message à afficher
	-Sortie : 
		un entier
"""
def selectionMotCoupe(message):
	l=input(message)
	while(l!="a" and l!="z"):
		print("Vous n'avez pas entré un caractère convenable. Ressayer")
		l=input(message)
	return l

"""
Objectif : Vérifie et renvoie l'entier entré par l'utilisateur
Paramètres :
	-Entrée :
		-message : Message à afficher
	-Sortie : 
		un entier
"""
def inputInt(input):
	while(True):
		try:
			entier=int(input)
			return True
		except:
			return False

def inputChar(message):
	char=input(message)
	while(True):
		try:
			char=char(entier)
			return char
		except:
			print("Vous n'avez pas entré une lettre. Réessayer")
			char=input(message)