import requests as requete #Permet de faire du HTTP
from bs4 import BeautifulSoup #Permet de parser du XML & HTML
import re as regex #Permet d'utiliser les expressions rationnelles
import time #Permet d'effectuer un sleep
import csv #Permet de manipuler des fichiers csv
import json #Permet de manipuler des fichiers json
import string #Permet de manipuler les chaînes de caractères

"""
Mode d'emploi du crawler 
	Rechercher le site qui contient les informations à récupérer
	Inspecter la page web pour identifier les balises qui contiennent l'information à récupérer
	Insérer le nom des balises et leur classe dans dicoInfos ( { infoARecup => [balise,classe/id] }, voir exemple plus bas )
	Vérifier si certaines informations ont besoin de nettoyage -> à préciser dans le tableau infosAEnlever
	Lancer le crawler

Attention : Le crawler principal peut-être très long d'exécution suivant la grosseur de la liste des mots passée en paramètre.
Soyez patient et n'hésitez pas à lancer plusieur crawler, en parralèle, chacun avec un intervalle de mots différents que vous pourrez
définir en apportant quelques retouches à la fonction getDictAsList.
De plus, penser bien à écrire les résultats dans des fichiers différents afin d'éviter des problèmes de partage de ressources, puis à
copier-coller les fichiers à la fin du fichier résultats. (aider vous des fichiers dicoFr,dicoFr2,dicoFr3.... déjà créés)

Remarque : Les fichiers résultats seront créés dans le répertoire Crawler/, penser bien à les déplacer dans les bons répertoires !
"""

#Retourne une liste ordonnée des éléments contenus dans fichierSource
def getDictAsList(fichierSource):
	i=0
	file = open(fichierSource, "r")
	dic = []
	lignes = file.readlines()
	for ligne in lignes:
		mot = ligne.rstrip('\n')
		dic.append(mot)
	return dic

#Permet de lire un fichier csv (utile pour les tests pour vérifier si le fichier a été correctement créé)
def lireCSV(fichier):
	with open(fichier,'r') as dico:
		dicoReader=csv.reader(dico,delimiter=',')
		i=0
		for row in dicoReader:
			if(i>100):
				break
			print(row[0] + ',' + row[1] + ',' + row[2] + ',' + row[3])
			a=row[3][2:-2].replace('\'','').split(',')
			print(a[0])
			i=i+1


#Récupère les classes grammaticales d'un mot pour la langue anglaise (c'était différent par rapport à la langue française)
def recupClassGramEn(soup,dicoInfos):
	categ=list()
	for classe in dicoInfos['id']: #pour chaque classe grammaticale
		c=soup.find(dicoInfos['classe'][0], {"id": classe})
		if c is not None: #on vérifie si le mot possède cette classe grammaticale
			categ.append(c)
	return categ



def crawlerLettre(listeMots,url,fichierDestination,dicoInfos):
	with open(fichier,'a') as dico: #on ouvre le fichier dans lequel on va écrire les résultats
		dicoWriter=csv.writer(dico,delimiter=',')
		for mot in listeMots:
			if(True):
			#try:
				r = requete.get(url) #On exécute une requête get
				page = r.content #On récupère le contenu de la réponse
				soup = BeautifulSoup(page,features="html.parser") #Va nous servir à parser la page
				prononciation = soup.find(dicoInfos['phon'][0], {"class": dicoInfos['phon'][1]}) # ( pour le français par exemple -> On recherche la première balise span qui a une class API )
				pron = prononciation.string.strip() #On enlève les balises html de la chaine
				pron = pron[1:-1] #On enlève les '\' en début et fin
				dicoWriter.writerow([mot,pron,"",list(dicoInfos['categLettre'])]) #écrit dans le fichier

				mot=mot + "'"
				r = requete.get(url) #On exécute une requête get
				page = r.content #On récupère le contenu de la réponse
				soup = BeautifulSoup(page,features="html.parser") #Va nous servir à parser la page
				prononciation = soup.find(dicoInfos['phon'][0], {"class": dicoInfos['phon'][1]}) # ( pour le français par exemple -> On recherche la première balise span qui a une class API )
				pron = prononciation.string.strip() #On enlève les balises html de la chaine
				pron = pron[1:-1] #On enlève les '\' en début et fin
				dicoWriter.writerow([mot,pron,"",list(dicoInfos['categPronom'])]) #écrit dans le fichier
			#except:
			else:
				print('Problème dans la recherche des noms' + mot)

"""
Récupère tous les prénoms/noms d'une langue.
Paramaètres :
	En entrée : 
		-url : url de la page web sur laquelle on va récupérer les informations
		-fichier : chemin du fichier dans lequel sera écris les résultats
		-dicoInfos : clé -> info à récupérer, valeurs -> contient les balises et leurs classes qui contienne l'infos
"""
def crawlerNom(url,fichierDestination,dicoInfos):
	with open(fichierDestination,'a') as file: #'a'-> écrit à partir de la fin du fichier sans effacer ce qu'il y avait déjà d'écris
		try:
			r = requete.get(url+mot) #On exécute une requête get
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
*-- Crawler principal --*
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
	with open(fichier,'a') as dico: #on ouvre le fichier dans lequel on va écrire les résultats
		dicoWriter=csv.writer(dico,delimiter=',')
		for mot in listeMot:
			#if(True):
			try:
				r = requete.get(url+mot) #On exécute une requête get
				page = r.content #On récupère le contenu de la réponse
				soup = BeautifulSoup(page,features="html.parser") #Va nous servir à parser la page
				prononciation = soup.find(dicoInfos['phon'][0], {"class": dicoInfos['phon'][1]}) # ( pour le français par exemple -> On recherche la première balise span qui a une class API )
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
					tabCateg.add(dicoInfos['nom']) #On insère 'nom propre' directement comme classe grammaticale
					tabCateg=list(tabCateg)
					dicoWriter.writerow([mot,pron,genre,tabCateg])
				else:
					#Suivant les langues il peut y avoir des différentes pour récupèrer les classes grammaticales
					if(langue=='fr'):
						#pour le français, il fallait préciser la classe de l'id de la balise
						categ=soup.find_all(dicoInfos['classe'][0], {"class": dicoInfos['classe'][1], "id": regex.compile(langue+"-*")}) #Récupère toutes les classes grammaticales d'un mot pour une langue donnée
					if(langue=='en'):
						#pour l'anglais il fallait que l'id
						categ=recupClassGramEn(soup,dicoInfos)
					#On nettoie les résultats
					for c in categ:
						c=c.string.strip().lower() #On enlève les balises html et on met en minuscule
						for infos in infosAEnlever:
							c=c.replace(infos,"") #Enlève les sous-chaînes inutiles
						tabCateg.add(c) 
								

					tabCateg=list(tabCateg) #Convertie en liste
					dicoWriter.writerow([mot,pron,genre,tabCateg]) #écrit dans le fichier
				compteur=compteur+1
				print("Mot : ",compteur) #juste pour suivre l'avancée lors de l'exécution
				if(compteur%1000==0):
					if(compteur%2000==0):
						time.sleep(60) #S'endort 0.1 seconde (permet d'éviter de se faire ban du site)
					else:
						time.sleep(30)
			#else:
			except:
				#Dans le cas où le mot n'est pas référencé sur wikitionnary, s'il n'a pas d'écriture phonétique etc...
				print("Dernier mot : ",compteur)
				print("Problème dans la recherche du mot : "+mot)




"""
Voici un exemple d'utilisation effectuée pour la langue française puis anglaise
N'hésitez pas à vous en inspirer si vous voulez ajouter une nouvelle langue
"""


"""
#Pour récupérer tous les prénoms de la langue française
fichierDestination="nomsFr.txt"
dicoInfos={"nom":['a','new']}
urlPrenom="https://fr.wikipedia.org/wiki/Liste_de_prénoms_en_français"
#crawlerNom(urlPrenom,fichierDestination,dicoInfos)
dicoInfos={"nom":['a','mw-disambig']}
urlNom="https://fr.wikipedia.org/wiki/Liste_des_noms_de_famille_les_plus_courants_en_France"
#crawlerNom(urlNom,fichierDestination,dicoInfos)
"""
"""
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

"""
#-> utile pour nettoyer le dictionnaire de certaines informations
#Ici, on enlève les 'pronom 1','pronom 2' ... 'pronom 9' par juste 'pronom', n'hésitez pas à vous renseigner sur la commande système sed (qui est très pratique pour faire des modifications rapidement sur le contenu d'un fichier !)
#cat data/fr/dicoFr.csv | sed -re 's/pronom [1-9]/pronom/g' > test.csv 

"""

#Pour la langue anglaise
"""
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

#lireCSV(fichier)
#print(len(listeMotAng))
#print(listeMotAng)
"""



listeMot= list(string.ascii_lowercase) #Liste qui contient les mots pour lesquels on veut récupérer leurs informations
for i in range(len(listeMot)):
	listeMot[i]=listeMot[i] + "'"

url="https://fr.wiktionary.org/wiki/" #l'url de la page à parser
dicoInfos={"phon" : ['span','API'],"nom": "lettre", "genre": ['div','div']}
fichier='dicoFr2.csv'
langue="fr"
crawler(listeMot,url,dicoInfos,[],langue,fichier,True)





#Partie : création des dictionnnaires par thème : 

"""
Récupère tous les mots suivant un thème
Paramaètres :
	En entrée : 
		-url : url de la page web sur laquelle on va récupérer les informations
		-fichierDestination : chemin du fichier dans lequel sera écris les résultats
		-dicoInfos : clé -> info à récupérer, valeurs -> contient les balises et leurs classes qui contienne l'infos
		-langue : langue courante
		-infosAEnlever : contient les informations à nettoyer
"""
def crawlerDicoTheme(url,fichierDestination,dicoInfos,langue,infosAEnlever):
	dico=[]
	for lettre in list(string.ascii_lowercase): #système de pagination utilisée sur wikitionnary
		newUrl=url+lettre #pour récupérer les mots de chaque lettre
		r = requete.get(newUrl) #On exécute une requête get
		page = r.content #On récupère le contenu de la réponse
		soup = BeautifulSoup(page,features="html.parser") #Va nous servir à parser la page
		noms=soup.find_all(dicoInfos['nom'][0], {"class": dicoInfos['nom'][1]})
		for n in noms:
			try:
				n=n.string.strip().lower()
				for info in infosAEnlever:
					n=n.replace(info,"")
				n=n.split()
				for i in range(len(n)):
					if(n[i] not in dico):
						dico.append(n[i])
			except:
				print("Problème dans la recherche")
	with open(fichierDestination,'w') as file2:
		json.dump(dico,file2)


"""
def recupererConjugaison(langue,fichierSource):
	with open(fichierSource) as vulgaire:
		BDInfo = json.load(vulgaire)
	with open(f'../data/{langue}/dicoClassGramm{langue.capitalize()}.json') as tmp:
		dicoClassGramm = json.load(tmp)
	verbe=""
	if(langue=='fr'):
		verbe="verbe"
	for word in BDInfo:
		try:
			if verbe in dicoClassGramm[word]:
				print(n + " est un verbe")
		except:
			print(word + " n'est pas un verbe")
			continue
"""

"""
Ici, on souhaite récupérer tous les mots qui ont un lien avec l'informatique pour la langue française
url="https://fr.wiktionary.org/w/index.php?title=Catégorie:Lexique_en_français_de_l'informatique&from="
langue="fr"
fichierDestination=f"DicoInformatique{langue}.json"
dicoInfos={"nom":['li',""]}
infosAEnlever=["d\u2019","j\u2019","l\u2019","m\u2019","s\u2019"] #pour enlever les apostrophes
#crawlerDicoTheme(url,fichierDestination,dicoInfos,langue,infosAEnlever)
"""