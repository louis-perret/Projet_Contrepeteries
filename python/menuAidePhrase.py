from echSyllabe import *
from utilitaires import *
import sys
import numpy as np

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
			a. Les lettres (la poule mue --> la moule pue)
			z. Les sons	(la chine et le nippons --> la pine et les nichons)
			e. Lettres et sons
			r. retour\n""")
		try:
			n = input()
		except ValueError:
			print("Vous n'avez pas saisie un caractère valide.\n")
		if n in ["a","z","e","r"]:
			if (n == "r"):
				return
			test = False
		else:
			print("Votre saisie n'est pas valide\n")

	while(True):
		print("a :quitter\nz revenir au menu précédant")
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
		boucle = True
		noPage = 1
		taillePage = 51
		nbPage = int(len(listeRes)/50)+1
		while(boucle):	
			if noPage < nbPage :
				res = affiRechFiltre(listeRes[taillePage*(noPage-1):taillePage*noPage-1],'word',isAllContrepeterie,noPage,nbPage,len(listeRes))
			else :
				res =affiRechFiltre(listeRes[taillePage*(noPage-1):],'word',isAllContrepeterie,noPage,nbPage,len(listeRes))
			if res == 2 :
				if noPage > 1 :
					noPage -= 1
			elif res == 3 :
				if noPage < nbPage :
					noPage += 1
			else :
				boucle = False

		if(isAllContrepeterie): #si l'utilisateur a choisi le mode qui fait tout
			return res #on renvoie directement les résultats car on ne veut pas faire l'affichage tout de suite
	else:											
		phraseOrigine = phrase.lower().replace("'"," ")
		phrasePhon = Phrase_to_Phon(phraseOrigine)

		#si un mot n'a pas pu être traduit
		if phrasePhon == False:
			input()
			return 1
		# retourne tout les combinaisons de phonemes qui marchent
		listeRes = mainMixSyllables(phrasePhon, mode,dicoDico)
		nvListe = {}
		dicoPhon = dicoDico['DicoPhon']
		boucle = True
		noPage = 1
		taillePage = 51
		nbPage = int(len(listeRes)/50)+1
		
		for i in listeRes[1:]:
			tmp = " ".join(i[0])#L'écriture phonétique de la phrase
			pos1 = i[1][0] #index 1
			pos2 = i[2][0] #index 2
			# Phon_to_Phrase ("phrase phon" + phrase origine(l))
			nvListe[tmp] = Phon_to_Phrase(tmp, phrase.split(" "), pos1, pos2,langue, dicoPhon) #Pour chaque phrase, on ressort toutes ses écritures possibles
		while(boucle):	
			if noPage < nbPage :
				res = affiRechFiltre(dict(list(nvListe.items())[taillePage*(noPage-1):taillePage*noPage-1]),'phon',isAllContrepeterie, noPage, nbPage,len(listeRes))
			else :
				res =affiRechFiltre(dict(list(nvListe.items())[taillePage*(noPage-1):]),'phon',isAllContrepeterie,noPage, nbPage, len(listeRes))
			if res == 2 :
				if noPage > 1 :
					noPage -= 1
			elif res == 3 :
				if noPage < nbPage :
					noPage += 1
			else :
				boucle = False


		if(isAllContrepeterie): #si l'utilisateur a choisi le mode qui fait tout
			return nvListe #on renvoie directement les résultats car on ne veut pas faire l'affichage tout de suite
		return res


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
			if (affiRechFiltre(listeResPhon,'phon',True, 1, 1, len(listeResPhon)) == 1) :
				continuer = 1
		else:
			print("\n")
			print("Pas de résultats pour l'échange avec les phonèmes")
			input("appuyer sur n'importe quelle touche pour retourner au menu.")
			continuer = 1
	return continuer

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
