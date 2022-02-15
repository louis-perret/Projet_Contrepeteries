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
	l=inputInt(message)
	while(l<-1):
		print("Vous n'avez pas entré un entier convenable. Ressayer")
		l=inputInt(message)
	return l


"""
Objectif : Renvoie la longueur sélectionner par l'utilisateur
Paramètres :
	-Entrée :
		-message : Message à afficher
	-Sortie : 
		un entier
"""
def selectionMotCoupe(message):
	l=inputInt(message)
	while(l!=0 and l!=1):
		print("Vous n'avez pas entré un entier convenable. Ressayer")
		l=inputInt(message)
	return l

"""
Objectif : Vérifie et renvoie l'entier entré par l'utilisateur
Paramètres :
	-Entrée :
		-message : Message à afficher
	-Sortie : 
		un entier
"""
def inputInt(message):
	entier=input(message)
	while(True):
		try:
			entier=int(entier)
			return entier
		except:
			print("Vous n'avez pas entré un entier. Réessayer")
			entier=input(message)