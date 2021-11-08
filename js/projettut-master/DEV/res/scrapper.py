import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup


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

def wikiScrapper():
	dic = getDictAsList()
	lastWordDone = getLastDone()
	index = dic.index(lastWordDone)
	size = str(len(dic))

	for mot in dic[index+1:]:
		requete = requests.get("https://fr.wiktionary.org/wiki/"+mot)
		page = requete.content
		soup = BeautifulSoup(page)
		prononciation = soup.find("span", {"class": "API"})
		try:
			pron = prononciation.string.strip()
			pron = pron[1:-1]

			#écrire dans le dictionnaire
			with open("dict_fr.csv", "a", encoding="utf-8") as fichier:
				writer = csv.writer(fichier)
				writer.writerow((mot, pron))

			print(mot+": "+pron)
		except:
			print("Prononciation inconnue pour: "+mot)

wikiScrapper()