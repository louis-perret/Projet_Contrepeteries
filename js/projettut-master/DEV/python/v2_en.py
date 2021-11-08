import pandas as pd
import numpy as np
import nltk


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
	filename = "dict_"+lang+".csv"
	"""import os
	dirname = os.path.dirname(__file__)
	filename = os.path.join(dirname, file)"""
	df = pd.read_csv(filename)

	dico = df.set_index('0')['1'].to_dict()
	for key in dico:
		dico[key] = dico[key].split()
	return dico

def getPhrase():
	phraseinput = input("Phrase: ")
	return phraseinput.split()

def genererContrepetrerie(phrase, dict, samePhraseOrder=False):
	for mot in phrase:
		if(mot not in dict):
			print('Unknown word: '+mot)
			return
	printType(phrase)

	for mot1 in phrase:
		index1 = phrase.index(mot1)
		phraseRestante = phrase[index1+1:]
		for mot2 in phraseRestante:
			for index_syl1 in range(len(dict[mot1])):
				for index_syl2 in range(len(dict[mot2])):
					testMot1 = list(dict[mot1])
					testMot2 = list(dict[mot2])
					print(testMot1)
					print(testMot2)
					if(testMot1[index_syl1] == testMot2[index_syl2]):
						continue
					testMot1[index_syl1], testMot2[index_syl2] = testMot2[index_syl2], testMot1[index_syl1]
					if(testMot1 in d.values() and testMot2 in d.values()):
						for key, value in dict.items():
							if(value == testMot1):
								key1 = key
							if(value == testMot2):
								key2 = key
						res = phrase.copy()
						index2 = phrase.index(mot2)
						res[index1] = key1
						res[index2] = key2
						print(res)
						printType(res)
						print()
	for word in d.values():
		print(word)

def getType(dict):
	from PyDictionary import PyDictionary
	dictionary=PyDictionary()
	for key in dict:
		res = dictionary.meaning(key)
		if(bool(res)):
			res = list(dictionary.meaning(key))
			res = list(res)
			print(key+": ")
			print(res)
		else:
			print(key+": not in dict")

def printType(text):
	text = ' '.join(text)
	text = nltk.word_tokenize(text)
	types = nltk.pos_tag(text)
	res = ""
	for tup in types:
		res = res + tup[1] + " "
	print(res)


phrase = getPhrase()
d = getDict('en')
genererContrepetrerie(phrase,d)
