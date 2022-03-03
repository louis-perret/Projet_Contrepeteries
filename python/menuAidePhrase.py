from echSyllabe import *
from utilitaires import *
import sys
"""
Objectif : Gère le mode recherche de contrepèterie dans les phrases
Paramètres :
	-Entrée :
		-langue : langue choisie par l'utilisateur
	-Sortie : 
		-int : choix de l'utilisateur pour la navigation
"""
def aideContrepetriePhrase(dicoDico,langue):
	test = True
	mode = {"a": 'word', "z": 'phon', "e": 'wordPhon'}
	n = 0
	while test:
		print("""\nVoulez-vous échanger \n
			a. Les lettres
			z. Les sons
			e. Tous les échanges possibles\n""")
		try:
			n = input()
		except ValueError:
			print("Vous n'avez pas saisie un caractère valide.\n")
		if n in ["a","z","e"]:
			test = False
		else:
			print("Votre saisie n'est pas valide\n")

	while(True):
		print("a :quitter / z revenir au menu précédant")
		phraseOrigine = input("Phrase à sonder :\n")
		if  phraseOrigine == "a" : #si la phrase est vide
			sys.exit()
		if phraseOrigine == "z":
			return 1

		if(mode[n] == 'word' or mode[n] == 'phon'):
			return rechercheContrepeteriesPhrase(phraseOrigine,mode[n],langue,dicoDico,False)
		else:
			return rechercheToutesContrepeteriesPhrase(phraseOrigine,langue,dicoDico)
# ------------------------------------------------------------------------------

			
"""
Objectif : Effectue un type de recherche (lettre ou phonème) sur une phrase
Paramètres :
	-Entrée :
		-phrase : phrase entrée par l'utilisateur
		-mode : 'word' -> échange de lettres, 'phon' -> échange de phonèmes
	-Sortie : 
		-historique : un tableau
"""
def rechercheContrepeteriesPhrase(phrase, mode, langue, dicoDico, isAllContrepeterie):
	if mode == 'word':
		listeRes = mainMixSyllables(phrase, mode,dicoDico)
		#phrase = phraseOrigine.split()
		#liste = circulaireMixSyllabes(phrase, 'word')
		listeRes = affiRechFiltre(listeRes,'word',isAllContrepeterie)

		if(isAllContrepeterie): #si l'utilisateur a choisi le mode qui fait tout
			return listeRes #on renvoie directement les résultats car on ne veut pas faire l'affichage tout de suite
		else:
			affichagePhraseLettre(listeRes)
	else:											
		phraseOrigine = phrase.lower().replace("'"," ")
		phrasePhon = Phrase_to_Phon(phraseOrigine)

		#si un mot n'a pas pu être traduit
		if phrasePhon == False:
			input()
			return 1
		# retourne tout les combinaisons de phonemes qui marchent
		liste = mainMixSyllables(phrasePhon, mode,dicoDico)

		nvListe = {}
		dicoPhon = dicoDico['DicoPhon']
		for i in liste[1:]:
			tmp = " ".join(i[0])#L'écriture phonétique de la phrase
			pos1 = i[1][0] #index 1
			pos2 = i[2][0] #index 2
			# Phon_to_Phrase ("phrase phon" + phrase origine(l))
			nvListe[tmp] = Phon_to_Phrase(tmp, phrase.split(" "), pos1, pos2,langue, dicoPhon) #Pour chaque phrase, on ressort toutes ses écritures possibles

		if(isAllContrepeterie): #si l'utilisateur a choisi le mode qui fait tout
			return nvListe #on renvoie directement les résultats car on ne veut pas faire l'affichage tout de suite
		return affiRechFiltre(nvListe,'phon',isAllContrepeterie)


"""
Objectif : Effectue une recherche de contrepèteries sur une phrase avec toutes les fonctionnalités disponibles sur l'application
Paramètres :
	-Entrée :
		-phrase : phrase entrée par l'utilisateur
		-langue : langue choisie par l"utilisateur
	-Sortie : 
		-int : choix de l'utilisateur
"""
def rechercheToutesContrepeteriesPhrase(phrase,langue, dicoDico):
	listeResWord = rechercheContrepeteriesPhrase(phrase,'word',langue, dicoDico, True)
	listeResPhon = rechercheContrepeteriesPhrase(phrase,'phon',langue, dicoDico, True)
	continuer=2
	while(continuer == 2):
		print("\nLes contrepétries possibles sont :\n")
		affichagePhraseLettre(listeResWord)
		if(listeResPhon != 1 ):
			print("\n")
			affiRechFiltre(listeResPhon,'phon',True)
		else:
			print("\n")
			print("Pas de résultats pour l'échange avec les phonèmes")
		
		continuer=choisirModeAffichage(f"a -> Quitter l'application, z -> Retour au menu : ")
		if(continuer == "a"):
			sys.exit()


"""
Objectif : Contrôle le choix de l'utilisateur
Paramètres :
	-Entrée :
		-message : message à afficher
	-Sortie : 
		-int : choix de l'utilisateur
"""
def choisirModeAffichage(message):
	choix=input(message)
	while(choix != "a" and choix != "z" and choix != "e"):
		choix=input(message)
	return choix
