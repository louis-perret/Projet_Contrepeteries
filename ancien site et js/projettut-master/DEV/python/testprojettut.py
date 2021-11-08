import random
import time
import os
import psutil
import matplotlib.pyplot as plt
from statistics import mean
import numpy as np
import math

#renvoie le dictionnaire des mots sous la forme d'un dictionnaire key = mot : value = mot
def getDictionnaire():
	#file = open("testdic.txt", "r")
	file = open("dic2.txt", encoding = "ISO-8859-1")
	dic = {}
	lignes = file.readlines()
	for ligne in lignes:
		mot = ligne.rstrip('\n')
		dic[mot]=mot
	return dic

#renvoie une liste de mot aléatoire à partir du dictionnaire
def getPhraseNulle():
	dic = getDictionnaire()
	phrasenulle = []
	nbMots = random.randint(3,10)
	for i in range(nbMots):
		phrasenulle.append(random.choice(list(dic.keys())))
	return phrasenulle

#test en affichant une phrase de mot généré aléatoirement
def testPhraseNulle():
	phrase = ""
	for mot in getPhraseNulle():
		if(phrase == ""):
			phrase = mot.title()
		else:
			phrase = phrase + " " + mot
	print(phrase)

def isConsonne(lettre):
	consonnes = {'b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z'}
	if(lettre in consonnes):
		return 1
	else:
		return 0

def motExiste(mot,dic):
	if(mot in dic):
		return True
	else:
		return False

#test si en échangeant les premières lettres, les mots existent
def swapFirstLetterExist(mot1,mot2,dic):
	#string to list char
	mot1splitted = list(mot1)
	mot2splitted = list(mot2)
	if(mot1splitted[0] == mot2splitted[0]):
		return 0
	#nouveaux mots
	mot1swap = mot1splitted.copy()
	mot1swap[0] = mot2splitted[0]
	mot2swap = mot2splitted.copy()
	mot2swap[0] = mot1splitted[0]
	mot1swapjoin = ''.join(mot1swap)
	mot2swapjoin = ''.join(mot2swap)


	if(motExiste(mot1swapjoin,dic) and motExiste(mot2swapjoin,dic)):
		return 1
	else:
		return 0

def listeMot():
	l=[]
	file = open("dic2.txt", encoding = "ISO-8859-1")
	lignes = file.readlines()
	for ligne in lignes:
		mot = ligne.rstrip('\n')
		l.append(mot)
	return l		

def v0():
	phraseinput = input("Phrase: ")
	dic = getDictionnaire()

	phrase = phraseinput.split()

	phraseRes = []
	for mot in phrase:
		phraseRes.append(list(mot))


	#pour chaque mot
	for mot in phrase:
		motsplitted = list(mot)
		#print(motsplitted)
		if(isConsonne(motsplitted[0])):
			#regarde les mots suivants en testant si en permuttant la premiere lettre, les 2 mots existent
			index = phrase.index(mot)
			for testmot in range(index+1,len(phrase)):
				if(swapFirstLetterExist(mot,phrase[testmot],dic)):
					lettre1 = phraseRes[index][0]
					phraseRes[index][0] = phraseRes[testmot][0]
					phraseRes[testmot][0] = lettre1

					phraseFinal = ""
					for mot in phraseRes:
						if(phraseFinal == ""):
							phraseFinal="".join(mot).capitalize()
						else:
							res = "".join(mot)
							phraseFinal = phraseFinal+' '+res
					print(phraseFinal)
					return

##### MAIN ######

#v0()

#start_time = time.time()

sett=getDictionnaire()
liste=listeMot()
lMoy=[]
N=100

start= time.time()

for i in range(N):
	start_time = time.time()

	for mot in liste:
		boole=motExiste(mot,sett)
		#print(boole)

	for i in range(200000):
		boole=motExiste("qererthrzth",sett)	
		#print(boole)


	print("Temps d execution : %s secondes ---" % (time.time() - start_time))
	process = psutil.Process(os.getpid())
	print(process.memory_info().rss)
	mem = psutil.virtual_memory()
	print(mem)
	lMoy.append((round((time.time()-start_time),4)))

mi=min(lMoy)
x=[]
while(mi < max(lMoy)):
	x.append(mi)
	mi=mi+0.0001

print("Temps d execution : %s secondes ---" % (time.time() - start))	

plt.hist(lMoy,bins = x)
plt.title('Test')
plt.xlabel('Temps d\'exécution en seconde')
plt.ylabel('Nombre d\'occurence')
plt.show()		

			




