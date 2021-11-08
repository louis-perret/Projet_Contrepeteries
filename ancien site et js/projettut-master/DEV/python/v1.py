import pandas as pd
import pyphen as ph #pip install pyphen
dic = ph.Pyphen(lang='fr')

def getFileNameCsv():
	import os
	dirname = os.path.dirname(__file__)
	filename = os.path.join(dirname, 'dico.csv')
	return filename;

def saveToCsv(df):
	df.to_csv(getFileNameCsv(),index=False)

def importCsv():
	return pd.read_csv(getFileNameCsv())

#Renvoie le dictionnaire des mots sous la forme d'un dictionnaire key = mot : value = mot
def getDictionnaire():
	file = open("dictionnaire.txt", "r")
	dic = []
	dic_syllabes = []
	lignes = file.readlines()
	for ligne in lignes:
		mot = ligne.rstrip('\n')
		dic.append(mot)
		dic_syllabes.append(getSyllabes([mot]))
	d = {'Mot': dic, 'Syllabes': dic_syllabes}
	df = pd.DataFrame(d)
	return df

""" Retourne les syllabes de la phrase.
Exemple, input: "camion poubelle"
Return: ['ca', 'mion', 'pou', 'belle']"""
def getSyllabes(phrase):
	phrase_syllabes = []
	for mot in phrase:
		res = dic.inserted(mot)
		res = res.split('-');
		for syllabe in res:
			phrase_syllabes.append(syllabe)
	return phrase_syllabes

def getPhrase():
	phraseinput = input("Phrase: ")
	return phraseinput.split()


######### MAIN #########
def toSet(syllabes):
	print(syllabes)


df = importCsv()
df['Syllabes'].apply(toSet)
