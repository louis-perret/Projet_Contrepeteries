from arbin import *
import json
import itertools
import sys
from commun import *

sys.stdout.reconfigure(encoding='utf-8')

###############################################################################
"""
Pour deux mots, teste toutes les combinaisons d'échanges possible entre ces deux mots
Renvoie une liste de type : (nouveauMot1,nouveauMot2,[i,j] du mot1,[i,j] du mot2)
"""

def mixSyllablesWord1(Word1, Word2, phrase, mode):
	listeWord = []
	tmp = []
	i = 0
	j = 0
	while(i < len(Word1)):

		[tmp, allResults] = mixSyllablesWord2(Word1[i:j], Word2, phrase, mode)

		for x in allResults :
			#listemot1 = mixSyllabeCoupe(Word1[:i] + x[1] + Word1[j:], mode)
			#listemot2 = mixSyllabeCoupe(x[0], mode)
			"""
			for l in listemot1 :
				for k in listemot2 :
					listeWord.append([l,k,[i,j],x[2]])
			"""
		for k in tmp:
			# test si retour de Word_to_Phon est une chaîne de caractère,
			# Si oui, alors le mélange est un mot existant
			if isInDico(mode, Word1[:i] + k[1] + Word1[j:]):
				listeWord.append([Word1[:i]+k[1]+Word1[j:], k[0], [i, j], k[2]])

		j += 1
		if (j > len(Word1)):
			i += 1
			j = i+1
	return listeWord

###############################################################################
"""
Créer un nouveau mot à partir de word2 en changeant ses lettres par la syllabe sy
Retourne une liste de résultat de type : (nouveauMot,ancienneSyllabe, le couple[i,j])
"""
def mixSyllablesWord2(sy, Word2, phrase, mode):
	i = 0
	j = 0
	liste = []
	allResults = []

	while(i < len(Word2)):
		# test si retour de Word_to_Phon est une chaîne de caractère
		# et si le Word trouvé n'est pas déjà dans la phrase d'origine.
		#if isInDico(mode, Word2[:i]+sy+Word2[j:]) and Word2[:i]+sy+Word2[j:] not in phrase: #le nouveau mot qu'on forme existe et n'est pas dans la phrase
		if isInDico(mode, Word2[:i]+sy+Word2[j:]):
			liste.append([Word2[:i]+sy+Word2[j:], Word2[i:j], [i, j]])
		# gestion de l'intervalle [i:j] section du Word2
		allResults.append([Word2[:i]+sy+Word2[j:], Word2[i:j], [i, j]])
		j += 1
		if j > len(Word2):
			i += 1
			j = i+1

	return liste, list(allResults)
###############################################################################
"""
prend en entrée la phrase de l'utilisateur,et le mode
soit 'phon' ou 'word' (même mode que pour isInDico)

retourne une liste de tuples de la forme :
(nvllePhrase,index1,index2)
index1 est un tuple contenant les coordonées dans la phrase
du premier mot que l'on échange
index2 est un tuple contenant les coordonées dans la phrase
du deuxième mot que l'on échange
"""

def mainMixSyllables(phrase, mode):

	phrase = phrase.split()
	print(phrase)
	Lphrases = [[phrase]] #phrase se contient elle même
	i = 0

	# Pour chaque mot dans la phrase
	for i in range(len(phrase)):
		# Pour chaque autre mot que tmp dans la phrase on permutra
		for j in range(i+1, len(phrase)):

			WordsContreP = mixSyllablesWord1(phrase[i], phrase[j], phrase, mode)
			WordsContreP = list(WordsContreP)
			# remplace les contreP trouvees dans la phrase
			for k in WordsContreP:
				tmp = phrase[:] #tous les éléments de phrase
		#ajoute les nouveaux mots au même endroit que les anciens
				tmp[i] = k[0] 
				tmp[j] = k[1]

				# pour chaque nouvelles combinaisons trouvées,
				# on vérifie que la nouvelles n'a pas déjà été trouvée
				taille = len(Lphrases)
				test = True
				for l in range(taille):
					if Lphrases[l][0] == tmp:
						test = False

				if test:
					L1 = (i, k[2][0], k[2][1])
					L2 = (j, k[3][0], k[3][1])
					Lphrases.append((tmp, L1, L2))
	return Lphrases

#------------------------------------------------------------------------------
"""
mixSyllabeCoupe
ajoute des espaces au mot échangé dans mixSyllablesWord1
"""


def mixSyllabeCoupe (word1, mode) :
	liste = []
	if len(word1) <= 1 :
		if isInDico(mode, word1) :
			liste.append(word1)
		return liste
	for i in range(1,len(word1)) :
		moitié1 = word1[0:i]
		moitié2 = word1[i:len(word1)]
		if isInDico(mode, moitié1) and isInDico(mode, moitié2) :
			if moitié1+" "+moitié2 not in liste :
				liste.append(moitié1+" "+moitié2)
		#if len(moitié1) > 1 : # ligne a échangé éventuellement par la prtie commentée
		moitié1 = mixSyllabeCoupe(moitié1, mode)
		#if len(moitié2) > 1 : # ligne a échanger éventuellement par la partie commentée
		moitié2 = mixSyllabeCoupe(moitié2, mode)
		for j in moitié1 :
			for k in moitié2 :
				if j+" "+k not in liste :
					liste.append(j+" "+k)
	return liste


"""
def mixSyllabeCoupe (word1, word2, mode, ij, ij2) :
	listefinal = []
	liste1 = []
	for j in range(len(word1)) :
		if (j < 1 and j > 0) or (j > len(word1)-1) :
			continue
		tmp10 = replacer(word1," ",j,0)
		tmp10 = tmp10.split(" ")
		tmp11 = tmp10[0]
		tmp12 = tmp10[1]
		for i in range(len(tmp11)) :
			if i < 1 and i > 0 or i > len(tmp11)-1 :
				continue
			tmp110 = replacer(tmp11," ",i,0)
			tmp110 = tmp110.split(" ")
			tmp111 = tmp110[0]
			tmp112 = tmp110[1]
			for k in range(len(tmp12)) :
				if k < 1 and k > 0 or k > len(tmp12)-1 :
					continue
				tmp120 = replacer(tmp12," ",k,0)
				tmp120 = tmp120.split(" ")
				tmp121 = tmp120[0]
				tmp122 = tmp120[1]
				if isInDico(mode, tmp11) and isInDico(mode, tmp121) and isInDico(mode, tmp122) :
					liste1.append(tmp11+" "+tmp121+" "+tmp122)
				if isInDico(mode, tmp111) and isInDico(mode, tmp112) and isInDico(mode, tmp121) and isInDico(mode, tmp122) :
					liste1.append(tmp111+" "+tmp112+" "+tmp121+" "+tmp122)
			if isInDico(mode, tmp111) and isInDico(mode, tmp112) and isInDico(mode, tmp12) :
				liste1.append(tmp111+" "+tmp112+" "+tmp12)
		if (isInDico(mode, tmp11) and isInDico(mode, tmp12)) or (tmp11 == "" and isInDico(mode, tmp12)) :
			liste1.append(tmp11+" "+tmp12)
	liste2 = secondeVerif(word2, mode)
	liste1 = list(set(liste1))
	liste2 = list(set(liste2))
	for l in enumerate(liste1) :
		for m in enumerate(liste2) :
			listefinal.append([l[1],m[1],ij,ij2])
	return listefinal


def secondeVerif (word2,mode) :
	liste = []
	for j in range(len(word2)) :
		if (j < 1 and j > 0) or (j > len(word2)-1) :
			continue
		tmp20 = replacer(word2," ",j,0)
		tmp20 = tmp20.split(" ")
		tmp21 = tmp20[0]
		tmp22 = tmp20[1]
		for i in range(len(tmp21)) :
			if i < 1 and i > 0 or i > len(tmp21)-1 :
				continue
			tmp210 = replacer(tmp21," ",i,0)
			tmp210 = tmp210.split(" ")
			tmp211 = tmp210[0]
			tmp212 = tmp210[1]
			for k in range(len(tmp22)) :
				if k < 1 and k > 0 or k > len(tmp22)-1 :
					continue
				tmp220 = replacer(tmp22," ",k,0)
				tmp220 = tmp220.split(" ")
				tmp221 = tmp220[0]
				tmp222 = tmp220[1]
				if isInDico(mode, tmp21) and isInDico(mode, tmp221) and isInDico(mode, tmp222) :
					liste.append(tmp21+" "+tmp221+" "+tmp222)
				if isInDico(mode, tmp211) and isInDico(mode, tmp212) and isInDico(mode, tmp221) and isInDico(mode, tmp222) :
					liste.append(tmp211+" "+tmp212+" "+tmp221+" "+tmp222)
			if isInDico(mode, tmp211) and isInDico(mode, tmp212) and isInDico(mode, tmp22) :
				liste.append(tmp211+" "+tmp212+" "+tmp22)
		if (isInDico(mode, tmp21) and isInDico(mode, tmp22)) or (tmp21 == "" and isInDico(mode, tmp22)) :
			liste.append(tmp21+" "+tmp22)
	return liste
"""
#------------------------------------------------------------------------------


"""
circulaireMixSyllabes
effectue des recherches circulaires dans une phrase
"""
"""
def circulaireMixSyllabes (phrase, mode):
	results = []
	for i in range(3, len(phrase)):
		for j in range(min(len(enumerate(phrase)))):
			for k in range(j, min(len(enumerate(phrase))))
				results.extends(circulaire(i,j,phrase,mode,[]))
	return results
"""
"""
def circulaire (i,j,k,phrase,mode,sylabePrec):
	results = []
	for mot in enumerate(phrase):
		for x in range(j, k) :
			for lettre in enumerate(mot): #Pour chaque lettre du mot
				coupleLettre=recupCouple(mot,x,lettre[0]) #on recupère le prochain couple de lettre à échanger
				if coupleLettre[0] :
					if sylabePrec is not None :
						nvtMot=replacer(mot,sylabePrec,lettre[0],x) #On remplace
						if coupleLettre[1] != couple and isInDico(mode, nvtMot):
							if i == 0 :
								results = [nvMot, coupleLettre]
								return results
							else :
								results = [nvMot].extend(circulaire(i-1,j,k,phrase.remove(mot),mode,coupleLettre))
								return results
					else :
						tmpResults = circulaire(i-1,j,k,phrase.remove(mot),mode,coupleLettre)
						nvMot = replacer(mot, results.pop(-1), lettre[0], x)
						if coupleLettre[1] != couple and isInDico(mode, nvtMot):
							results = [nvMot].extend(tmpResults)
							return results
				
"""




###############################################################################
"""
Retourne liste de phonème de la phrase :
'la poule qui mu' -> 'la pul ki my
"""
def Phrase_to_Phon(phrase):
	string = ''
	for mot in phrase.split():
		b=Mot_to_Phon_Only(arbre_mot, mot)
		if b != False:
			string += b + ' '
		else:
			print('\nLe mot', mot, '''de la phrase n\'est pas dans notre dictonnaire.
			Veuillez essayer avec une autre orthographe.''')
			return False
			break
	return string

################################################################################
'''
Prend en argument une phrase en phonétique en string
retourne les combinaisons possibles de phrases en orthographe
classique en string
phraseOrigine est la liste des mots de la phrase d'origine,
on l'utilise pour filtrer les resultats des combinaisons
selon un % de mots recurrent entre la nvlle et l'ancienne phrase
'''

def Phon_to_Phrase(PhrasePhoneme, phraseOrigine, pos1, pos2,langue):

	listeretour = []
	listePhon = PhrasePhoneme.split()
	# PhrasePhoneme(str)
	with open(f'data/{langue}/dicoPhoncom{langue.capitalize()}.json') as tmp:
		dicoPhon = json.load(tmp)

# Extraction du dico de phonème les mots possible a partir des phonèmes en entrée
	for i in range(len(listePhon)):
		listePhon[i] = dicoPhon[listePhon[i]] #Pour chaque phonème de la phrase, on récupère tous les mots qui s'écrivent pareil

	for i in range(len(listePhon[pos1])):
		for j in range(len(listePhon[pos2])):
			string = phraseOrigine[:]
			string[pos1] = listePhon[pos1][i]
			string[pos2] = listePhon[pos2][j]

			listeretour.append(string)


# Produit de toutes les combinaisons possibles des mots
# qui ont changer par rapport à la phrase d'origine
	return listeretour
