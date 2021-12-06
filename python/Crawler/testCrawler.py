import requests as requete #Permet de faire du HTTP
from bs4 import BeautifulSoup #Permet de parser du XML & HTML
import re as regex #Permet d'utiliser les expressions rationnelles
import time
import csv #Permet de manipuler des fichiers csv

#Retourne une liste ordonné tel le fichier dictionnaire.txt
def getDictAsList(fichierSource):
	i=0
	file = open(fichierSource, "r")
	dic = []
	lignes = file.readlines()
	for ligne in lignes:
		if(i>=100):
			break
		mot = ligne.rstrip('\n')
		dic.append(mot)
		i=i+1
	return dic

#Permet de lire un fichier csv (utile pour les tests)
def lireCSV(fichier):
	with open(fichier,'r') as dico:
		dicoReader=csv.reader(dico,delimiter=',')
		for row in dicoReader:
			print(row[0])
			print(row[1])
			print(row[2])
			a=row[3][2:-2].replace('\'','').split(',')
			print(a)

"""
Récupère l'écriture phonétique, le genre et toutes les classes grammaticales des mots d'une langue.
Paramaètres :
	En entrée : 
		-listeMot : liste qui contient tous les mots sur lesquels va s'appuyer le crawler
		-url : url de la page web sur laquelle on va récupérer les informations
		-dicoInfos : clé -> info à récupérer, valeurs -> contient les balises et leurs classes qui contienne l'infos
		-infosAEnlever : contient les chaînes de caractères à enlever (pour la recherche des classes grammaticales suivant les langues)
		-langue : langue des mots
		-fichier : chemin du fichier dans lequel sera écris les résultats
"""
def crawler(listeMot,url,dicoInfos,infosAEnlever,langue,fichier):
	with open(fichier,'w') as dico:
		dicoWriter=csv.writer(dico,delimiter=',')
		for mot in listeMot:
			try:
				r = requete.get(url+mot) #On exécute une requête get
				page = r.content #On récupère le contenu de la réponse
				soup = BeautifulSoup(page,features="html.parser") #Va nous servir à parser la page
				prononciation = soup.find(dicoInfos['phon'][0], {"class": dicoInfos['phon'][1]}) #On recherche la première balise span qui a une class API
				pron = prononciation.string.strip() #On enlève les balises html de la chaine
				pron = pron[1:-1] #On enlève les '\' en début et fin
				
				genre=soup.find(dicoInfos['genre'][0],{"class": dicoInfos['genre'][1]})
				if(genre != None):
					genre=genre.string.strip()
					genre=genre[0] #On récupère que la première lettre (soit 'm' soit 'f')

				if genre != 'm' and genre != 'f': #Si le mot n'a pas de genre
					genre=""
			
				tabCateg=set() #Permettra d'éviter les doublons
				categ=soup.find_all(dicoInfos['classe'][0], {"class": dicoInfos['classe'][1], "id": regex.compile(langue+"-*")}) #Récupère toutes les classes grammaticales d'un mot pour une langue donnée
				for c in categ:
					c=c.string.strip().lower()
												
					for infos in infosAEnlever:
						c=c.replace(infos,"") #Enlève les sous-chaînes inutiles
					tabCateg.add(c) 
							

				tabCateg=list(tabCateg) #Convertie en liste
				dicoWriter.writerow([mot,pron,genre,tabCateg]) #écrit dans le fichier
				time.sleep(0.1) #S'endort 0.1 seconde (permet d'éviter de se faire ban)
			except:
				print("Problème dans la recherche du : "+mot)


#Pour la langue française
fichierSource='dictionnaire.txt'
listeMot=getDictAsList(fichierSource) #Liste qui contient les mots pour lesquels on veut récupérer leurs informations
url="https://fr.wiktionary.org/wiki/" #l'url de la page à parser
dicoInfos={"phon" : ['span','API'], "genre" : ['span','ligne-de-forme'], "classe" : ["span","titredef"]} 
#Dico avec comme clé l'information à récupérer et comme valeur la balise html et la classe css qui la contient
infosAEnlever=["forme de ","forme d’"," commun"] #On récupère 'forme de verbe' -> on aura 'verbe' à la fin
langue='fr'
fichier='dicoFr.csv'
crawler(listeMot,url,dicoInfos,infosAEnlever,langue,fichier)
lireCSV(fichier)