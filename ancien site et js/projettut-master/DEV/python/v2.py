import pandas as pd
import numpy as np
import copy
import unicodedata
from math import floor
#nltk.download('wordnet')

# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()


def saveToCsv(df,filename):
	df.to_csv(filename,index=False)

def generate_dict():
	from big_phoney import BigPhoney

	#txt -> dict = {}
	file = open("dict_en.txt", "r")
	dic = {}
	lignes = file.readlines()
	for ligne in lignes:
		mot = ligne.rstrip('\n')
		dic[mot] = ''

	phoney = BigPhoney()

	c = '0'
	for mot in dic:
		if(c != mot[0]):
			c = mot[0]
			print(mot)
		dic[mot] = (phoney.phonize(mot)).split()

	df = pd.DataFrame(list(dic.items()))
	saveToCsv(df,'dict_en.csv')

def getDict(lang):
	filename = "../res/dict_"+lang+".csv"
	"""import os
	dirname = os.path.dirname(__file__)
	filename = os.path.join(dirname, file)"""
	df = pd.read_csv(filename)

	dico = df.set_index('0')['1'].to_dict()
	for key in dico:
		dico[key] = dico[key].split()
	return dico

	return dico

def getPhrase():
	phraseinput = input("Phrase: ")
	return phraseinput.split()

def printRes(phrase, dict):
	pronList = []
	for mot in phrase:
		pronList.append(dict[mot])
	print(pronList)


def listerChar():
	d = getDict('fr_ok')
	res = set()
	for key in d:
		chars = list("".join(d[key]))
		for char in chars:
			if(char not in res):
				res.add(char)

	with open('all_char.txt','w') as f:
   		f.write(str(res))


"""def splitPron(pron):
	l = []
	for char in pron:
		if(char in )"""

def splitCombining(s):
	l = []
	tmp =''
	for c in s:
		if(unicodedata.combining(c)!=0):
			if(len(l)==0):
				tmp += c
			else:
				l[-1] += c
		else:
			if(tmp==''):
				l.append(c)
			else:
				tmp += c
				l.append(tmp)
				tmp =''
	return l

def flatDict(d):
	for key in d:
		word = []
		for syllabe in d[key]:
			word.append(splitCombining(syllabe))
		d[key] = [val for sublist in word for val in sublist]
	return d


def genererContrepetrerie(phrase, dict):
	for mot in phrase:
		if(mot not in dict):
			print('Unknown word: '+mot)
			return

	printRes(phrase, dict)
	print()

	for mot1 in phrase:
		index1 = phrase.index(mot1)
		phraseRestante = phrase[index1+1:]
		for mot2 in phraseRestante:
			pron = list("".join(dict[mot2]))
			for index_syl1 in range(len(dict[mot1])):
				for index_syl2 in range(len(dict[mot2])):
					testMot1 = list(dict[mot1])
					testMot2 = list(dict[mot2])
					if(testMot1[index_syl1] == testMot2[index_syl2]):
						continue
					testMot1[index_syl1], testMot2[index_syl2] = testMot2[index_syl2], testMot1[index_syl1]
					if(testMot1 in d.values() and testMot2 in d.values()):
						key1 = set()
						key2 = set()
						for key, value in dict.items():
							if(value == testMot1):
								key1.add(key)
							if(value == testMot2):
								key2.add(key)
						res = phrase.copy()
						index2 = phrase.index(mot2)
						for word1 in key1:
							for word2 in key2:								
								res[index1] = word1
								res[index2] = word2
								print(res)
						print()

def generer(phrase,d,types):
	for mot in phrase:
		if(mot not in d):
			print('Mot inconnu: '+mot)
			return

	pronList = []
	for mot in phrase:
		pronMot = []
		for syllabe in d[mot]:
			pronMot.append(splitCombining(syllabe))
		pronMot = [val for sublist in pronMot for val in sublist]
		pronList.append(pronMot)

	items = d.items()
	values = d.values()

	#pour chaque index prononciation d'un mot de la phrase
	for wordIndex in range(len(pronList)):
		#pour 1 à la taille de la prononciation du mot en cours
		for sizeItem in range(1,len(pronList[wordIndex])):
			for swapIndexFirst in range(len(pronList[wordIndex])-sizeItem+1):
				#on échange dans le mot
				pass
				
				#on échange dans chaque autre mot restant
				for remainingWordIndex in range(wordIndex+1,len(pronList)):
					if(sizeItem <= len(pronList[remainingWordIndex])):
						for swapIndexSecond in range(len(pronList[remainingWordIndex])-sizeItem+1):
							pronListTest = copy.deepcopy(pronList)
							if(pronListTest[remainingWordIndex][swapIndexSecond:swapIndexSecond+sizeItem] == pronListTest[wordIndex][swapIndexFirst:swapIndexFirst+sizeItem]):
								#si les 2 syllabes à échanger sont identiques, continuer
								continue
							pronListTest[remainingWordIndex][swapIndexSecond:swapIndexSecond+sizeItem], pronListTest[wordIndex][swapIndexFirst:swapIndexFirst+sizeItem] = pronList[wordIndex][swapIndexFirst:swapIndexFirst+sizeItem], pronList[remainingWordIndex][swapIndexSecond:swapIndexSecond+sizeItem]

							#si true, contrepètrerie trouvée
							if(pronListTest[wordIndex] in values and pronListTest[remainingWordIndex] in values):
								#affichage résultat
								keys1, keys2 = getRes(items,pronListTest[wordIndex],pronListTest[remainingWordIndex])
								p = copy.deepcopy(phrase)
								p[wordIndex] = keys1
								p[remainingWordIndex] = keys2
								checkRes(p,"normal: ")
								continue

							#si le mot droit est bon
							if(pronListTest[remainingWordIndex] in values):
								#pour first, flat avec voisin de gauche :
								if(wordIndex > 0):
									flatVoisinGaucheFirst = [item for sublist in pronListTest[wordIndex-1:wordIndex+1] for item in sublist]
									keys1, keys2 = testerVoisin(flatVoisinGaucheFirst,items,values)
									if(keys1 != None):
										p = copy.deepcopy(phrase)
										p[remainingWordIndex] = getResUnique(items,pronListTest[remainingWordIndex])
										p[wordIndex-1] = keys2
										p[wordIndex] = keys1
										checkRes(p,"avec voisin gauche du mot1: ")
								
								if(wordIndex < len(pronListTest)+1):
									flatVoisinDroiteFirst = [item for sublist in pronListTest[wordIndex:wordIndex+2] for item in sublist]
									keys1, keys2 = testerVoisin(flatVoisinDroiteFirst,items,values)
									if(keys1 != None):
										p = copy.deepcopy(phrase)
										p[remainingWordIndex] = getResUnique(items,pronListTest[remainingWordIndex])
										p[wordIndex] = keys2
										p[wordIndex+1] = keys1
										checkRes(p,"avec voisin droit du mot1: ")

							#si le mot gauche est bon
							if(pronListTest[wordIndex] in values):
								#pour first, flat avec voisin de gauche :
								if(remainingWordIndex > 0):
									flatVoisinGaucheSecond = [item for sublist in pronListTest[remainingWordIndex-1:remainingWordIndex+1] for item in sublist]
									keys1, keys2 = testerVoisin(flatVoisinGaucheSecond,items,values)
									if(keys1 != None):
										p = copy.deepcopy(phrase)
										p[wordIndex] = getResUnique(items,pronListTest[wordIndex])
										p[remainingWordIndex-1] = keys2
										p[remainingWordIndex] = keys1
										checkRes(p,"avec voisin gauche du mot2: ")
									
								if(remainingWordIndex < len(pronListTest)-1):
									flatVoisinDroiteSecond = [item for sublist in pronListTest[remainingWordIndex:remainingWordIndex+2] for item in sublist]
									keys1, keys2 = testerVoisin(flatVoisinDroiteSecond,items,values)
									if(keys1 != None):
										p = copy.deepcopy(phrase)
										p[wordIndex] = getResUnique(items,pronListTest[wordIndex])
										p[remainingWordIndex] = keys2
										p[remainingWordIndex+1] = keys1
										checkRes(p,"avec voisin droit du mot2: ")

def checkRes(p,label = ""):
	for mots in p:
		if isinstance(mots,str):
			if 'vbc' in types[mots]:
				print(label,p)
		else:
			for mot in mots:
				if 'vbc' in types[mot]:
					print(label,p)
	#print(label,p)

def testerVoisin(flat,items,values):
	for index in range(1,len(flat)):
		mot1 = flat[index:]
		mot2 = flat[:index]
		if(mot1 in d.values() and mot2 in d.values()):
			return getRes(items,mot1,mot2)
	return None, None

def getRes(items,pronWord1,pronWord2):
	keys1 = set()
	keys2 = set()
	print(pronWord1, pronWord2)
	for key, value in items:
		if(value == pronWord1):
			keys1.add(key)
		if(value == pronWord2):
			keys2.add(key)
	return keys1, keys2

def getResUnique(items,pronWord):
	print("tessst",pronWord)
	keys = set()
	for key, value in items:
		if(value == pronWord):
			keys.add(key)
	return keys

def genererBis(phrase,d):
	for mot in phrase:
		if(mot not in d):
			print('Mot inconnu: '+mot)
			return

	sentencePron = []
	pronList = []
	for mot in phrase:
		sentencePron.append(splitCombining(d[mot]))
		for syllabe in d[mot]:
			pronList.append(splitCombining(syllabe))
	pronList = [val for sublist in pronList for val in sublist]
	"""sonTotale = len(pronList)
	#on echange d'abbord tous les sons uniques puis 2 etc
	for swapLen in range(1,floor(sonTotale/2)):
		for index1 in range(0,sonTotale-swapLen-2):
			for index2 in range(index1+1,sonTotale-swapLen-1):
				#on copie la liste initiale
				pronListTest = list.copy(pronList)
				#on swap
				pronListTest[index1:index1+swapLen], pronListTest[index2:index2+swapLen] = pronListTest[index2:index2+swapLen], pronListTest[index1:index1+swapLen]
				checkSentence(pronListTest,d)"""

def testerVoisins():
	pass

def checkSentence(inputList,d):
	wordList = d.keys()
	pronList = list(d.values())

	res = checkSentenceRecursive(inputList,pronList)
	if(res is not None):
		print(res)

def checkSentenceRecursive(inputList,pronList):
	if(len(inputList) == 0):
		return []

	#sons testés
	tried_so_far = []
	#pour chaque son dans la liste en entrée
	resList = []
	for pronIndex in range(len(inputList)):
		tried_so_far.append(inputList[pronIndex])
		if(tried_so_far in pronList):
			current_index = len(tried_so_far)
			res = checkSentenceRecursive(inputList[current_index:],pronList)
			if(res is not None):
				res.insert(0,"".join(tried_so_far))
				resList.append(res)
	return resList


def getTypes():
	df = pd.read_csv("../res/dict_fr_type.csv")

	dico = df.set_index('0')['1'].to_dict()
	for key in dico:
		if isinstance(dico[key],float):
			dico[key] = set()
		else:
			tmp = dico[key]
			dico[key] = set()
			for t in tmp.split():
				dico[key].add(t)
	return dico

def convertDictOk():
	with open("dict_fr.csv", "r") as f:
		lines = f.readlines()

	dic = {}
	for line in lines:
		word = line.split(',')
		pron = ' '.join(' '.join(word[1][:-1].split('.')).split())
		if "(" in pron:
			print(pron)
			pron = pron.replace("(", "")
			pron = pron.replace(")", "")
			print(pron)
		dic[word[0]] = pron


	df = pd.DataFrame(list(dic.items()))
	df.to_csv('dict_fr_ok.csv',index=False)

phrase = getPhrase()
d = getDict('fr_ok')
d = flatDict(d)
types = getTypes()
generer(phrase,d,types)
