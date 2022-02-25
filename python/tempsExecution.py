import math
import os
import json
import platform

def calculTempsExecution(longueurMot,longueurCoupleLettre,mode):
	if platform.system() == "Linux":
		with open('data/config.json','r') as diconfig_:
			dicoConfig = json.load(diconfig_)
			langue=dicoConfig['langue'] #on récupère la langue entrée par l'utilisateur
		liste = getDictAsList(f"./data/{langue}/dico{langue.capitalize()}.csv")
		loga = math.log(len(liste),10)
		os.system(f"./shellExec.sh {longueurMot} {longueurCoupleLettre} {int(loga)} {mode}")


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