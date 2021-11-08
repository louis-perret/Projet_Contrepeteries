import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
from threading import Thread

#Retourne une liste ordonné tel le fichier dictionnaire.txt
def getDictAsList():
	file = open("dictionnaire.txt", "r", encoding="utf-8")
	dic = []
	lignes = file.readlines()
	for ligne in lignes:
		mot = ligne.rstrip('\n')
		dic.append(mot)
	return dic

#Retourne le dernier mot scrappé
def getLastDone():
	with open("dict_fr_type.csv", "r") as f:
		#Dernière ligne en enlevant \n
		return f.readlines()[-1:][0][0:-1].split(',')[0]

"""
vb : verbe
vbc : verbe conjugué
nc : nom commun
adv : adverbe
adj : adjectif
cj : conjonction
"""

def listerType():
	res = set()
	for key in d:
		chars = list("".join(d[key]))
		for char in chars:
			if(char not in res):
				res.add(char)

	

def thread_function(mot, result, index):
	adresse = "https://fr.wiktionary.org/wiki/"+mot
	print(type(adresse))
	requete = requests.get("https://fr.wiktionary.org/wiki/"+mot)
	page = requete.content
	soup = BeautifulSoup(page)
	types = set()
	if(soup.find(title="Catégorie:Verbes en français") is not None):
		types.add("vb")
	if(soup.find(title="Catégorie:Formes de verbes en français") is not None):
		types.add("vbc")
	if(soup.find(title="Catégorie:Adjectifs en français") is not None):
		types.add("adj")
	if(soup.find(title="Catégorie:Formes d’adjectifs en français") is not None):
		types.add("adj")		
	if(soup.find(title="Catégorie:Noms communs en français") is not None):
		types.add("nc")
	if(soup.find(title="Catégorie:Formes de noms communs en français") is not None):
		types.add("nc")		
	if(soup.find(title="Catégorie:Conjonctions en français") is not None):
		types.add("cj")
	if(soup.find(title="Catégorie:Adverbes en français") is not None):
		types.add("adv")
	#set de type
	result[index] = types

def wikiScrapper():
	dic = getDictAsList()
	#lastWordDone = getLastDone()
	#index = dic.index(lastWordDone)
	index = 0
	nb = 10

	for i in range(index+1, len(dic), nb):
		threads = [None] * nb
		results = [None] * nb

		for j in range(nb):
			threads[j] = Thread(target=thread_function, args=(dic[i+j], results, j))
			threads[j].start()

		# do some other stuff

		for j in range(nb):
			threads[j].join()
			if(results[j] != None):
				with open("dict_fr_type.csv", "a", encoding="utf-8") as fichier:
					writer = csv.writer(fichier)
					res = ""
					for t in results[j]:
						res += t + " "

					writer.writerow((dic[i+j], res))

				#print(dic[i+j]+": "+results[j])

def convertDict():
	from collections import OrderedDict
	with open("dict_fr.csv", "r") as f:
		lines = f.readlines()

	dic = {}
	for line in lines:
		word = line.split(',')
		pron = ' '.join(' '.join(word[1][:-1].split('.')).split())
		print(pron)
		dic[word[0]] = pron


	df = pd.DataFrame(list(dic.items()))
	df.to_csv('dict_fr_ok.csv',index=False)
	


wikiScrapper()