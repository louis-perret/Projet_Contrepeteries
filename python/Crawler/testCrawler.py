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
		if(i>=20000):
			if(i>=30000):
				break
			mot = ligne.rstrip('\n')
			dic.append(mot)
		i=i+1
	return dic

#Permet de lire un fichier csv (utile pour les tests)
def lireCSV(fichier):
	with open(fichier,'r') as dico:
		dicoReader=csv.reader(dico,delimiter=',')
		i=0
		for row in dicoReader:
			if(i>100):
				break
			print(row[0] + ',' + row[1] + ',' + row[2] + ',' + row[3])
			#print(row[1])
			#print(row[2])
			#print(row[3])
			a=row[3][2:-2].replace('\'','').split(',')
			print(a[0])
			i=i+1



def recupClassGramEn(soup,dicoInfos):
	categ=list()
	for classe in dicoInfos['id']:
		c=soup.find(dicoInfos['classe'][0], {"id": classe})
		if c is not None:
			categ.append(c)
	return categ


"""
Récupère tous les prénoms d'une langue.
Paramaètres :
	En entrée : 
		-url : url de la page web sur laquelle on va récupérer les informations
		-fichier : chemin du fichier dans lequel sera écris les résultats
		-dicoInfos : clé -> info à récupérer, valeurs -> contient les balises et leurs classes qui contienne l'infos
"""
def crawlerNom(url,fichierDestination,dicoInfos):
	with open(fichierDestination,'a') as file: #'a'-> écris à partir de la fin du fichier sans effacer ce qu'il y avait déjà d'écris
		try:
			r = requete.get(url) #On exécute une requête get
			page = r.content #On récupère le contenu de la réponse
			soup = BeautifulSoup(page,features="html.parser") #Va nous servir à parser la page
			noms=soup.find_all(dicoInfos['nom'][0], {"class": dicoInfos['nom'][1]})
			for n in noms:
				n=n.string.strip().lower()
				n=n.title() #Met le premier caractère en majuscule
				file.write(n+'\n')
		except:
			print('Problème dans la recherche des noms')

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
		-isNom : booléen, si True -> on recherche que pour les noms propres d'une langue (pour la catégorie)
"""
def crawler(listeMot,url,dicoInfos,infosAEnlever,langue,fichier,isNom):
	compteur=0
	with open(fichier,'a') as dico:
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
				if(isNom): #Si on recherche pour les noms propres
					tabCateg.add(dicoInfos['nom'])
					tabCateg=list(tabCateg)
					dicoWriter.writerow([mot,pron,genre,tabCateg]) #on met comme catégorie nom propre
				else:
					if(langue=='fr'):
						categ=soup.find_all(dicoInfos['classe'][0], {"class": dicoInfos['classe'][1], "id": regex.compile(langue+"-*")}) #Récupère toutes les classes grammaticales d'un mot pour une langue donnée
					if(langue=='en'):
						categ=recupClassGramEn(soup,dicoInfos)
					for c in categ:
						c=c.string.strip().lower()
						for infos in infosAEnlever:
							c=c.replace(infos,"") #Enlève les sous-chaînes inutiles
						tabCateg.add(c) 
								

					tabCateg=list(tabCateg) #Convertie en liste
					dicoWriter.writerow([mot,pron,genre,tabCateg]) #écrit dans le fichier
				compteur=compteur+1
				print("Mot : ",compteur)
				if(compteur%1000==0):
					if(compteur%2000==0):
						time.sleep(60) #S'endort 0.1 seconde (permet d'éviter de se faire ban)
					else:
						time.sleep(30)
			except:
				print("Dernier mot : ",compteur)
				print("Problème dans la recherche du mot : "+mot)



"""
#Pour récupérer tous les prénoms de la langue française
fichierDestination="nomsFr.txt"
dicoInfos={"nom":['a','new']}
urlPrenom="https://fr.wikipedia.org/wiki/Liste_de_prénoms_en_français"
#crawlerNom(urlPrenom,fichierDestination,dicoInfos)
dicoInfos={"nom":['a','mw-disambig']}
urlNom="https://fr.wikipedia.org/wiki/Liste_des_noms_de_famille_les_plus_courants_en_France"
#crawlerNom(urlNom,fichierDestination,dicoInfos)

#Pour la langue française
fichierSource='nomsFr.txt'
listeMot=getDictAsList(fichierSource) #Liste qui contient les mots pour lesquels on veut récupérer leurs informations
url="https://fr.wiktionary.org/wiki/" #l'url de la page à parser
dicoInfos={"phon" : ['span','API'], "genre" : ['span','ligne-de-forme'], "classe" : ["span","titredef"],"nom": "nom propre"} 
#Dico avec comme clé l'information à récupérer et comme valeur la balise html et la classe css qui la contient
infosAEnlever=["forme de ","forme d’"," commun"] #On récupère 'forme de verbe' -> on aura 'verbe' à la fin
langue='fr'
fichier='nomsFr.csv'
"""

#Pour la langue anglaise
fichierSourceAng='nomsEn.txt'
listeMotAng=getDictAsList(fichierSourceAng) #Liste qui contient les mots pour lesquels on veut récupérer leurs informations
urlAng="https://en.wiktionary.org/wiki/" #l'url de la page à parser
dicoClasse=['Noun','Letter','Verb','Adverb','Adjective','Interjection','Preposition','Conjunction','Pronoun']
dicoInfosAng={"phon" : ['span','IPA'], "genre" : ['span','API'], "classe" : ["span","mw-headline"],"nom": "proper noun","id": dicoClasse} 
#Dico avec comme clé l'information à récupérer et comme valeur la balise html et la classe css qui la contient
infosAEnleverAng=["/"]#["forme de ","forme d’"," commun"] #On récupère 'forme de verbe' -> on aura 'verbe' à la fin
langue='en'
fichier='dicoFr.csv'
#crawler(listeMotAng,urlAng,dicoInfosAng,infosAEnleverAng,langue,fichier,True)

lireCSV(fichier)
#print(len(listeMotAng))
#print(listeMotAng)

#cat data/fr/dicoFr.csv | sed -re 's/pronom [1-9]/pronom/g' > test.csv 
