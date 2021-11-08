import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
from threading import Thread

#Retourne une liste ordonné tel le fichier dictionnaire.txt
def getDictAsList():
	file = open("dictionnaire.txt", "r")
	dic = []
	lignes = file.readlines()
	for ligne in lignes:
		mot = ligne.rstrip('\n')
		dic.append(mot)
	return dic

#Retourne le dernier mot scrappé
def getLastDone():
	with open("dict_fr.csv", "r") as f:
		#Dernière ligne en enlevant \n
		return f.readlines()[-1:][0][0:-1].split(',')[0]

def thread_function(mot, result, index):
	requete = requests.get("https://fr.wiktionary.org/wiki/"+mot)
	page = requete.content
	soup = BeautifulSoup(page)
	prononciation = soup.find("span", {"class": "API"})
	try:
		pron = prononciation.string.strip()
		pron = pron[1:-1]
		result[index] = pron
	except:
		print("Prononciation inconnue pour: "+mot)

def wikiScrapper():
	dic = getDictAsList()
	lastWordDone = getLastDone()
	index = dic.index(lastWordDone)
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
				with open("dict_fr.csv", "a", encoding="utf-8") as fichier:
					writer = csv.writer(fichier)
					writer.writerow((dic[i+j], results[j]))

				print(dic[i+j]+": "+results[j])

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
	


convertDict()