
def getDictionnaire():
	#file = open("testdic.txt", "r")
	file = open("dic2.txt", encoding = "ISO-8859-1")
	dic = {}
	lignes = file.readlines()
	for ligne in lignes:
		mot = ligne.rstrip('\n')
		dic[mot]=mot
	return dic

def motExiste(mot,dic):
	if(mot in dic):
		return True
	else:
		return False

	

def existSwapAllLetter(mot, dic):
	print(mot)
	l=[]
	alph=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	m=list(mot)
	motswap = m.copy()
	for j in range(len(motswap)):
		for i in alph:
			motswap = m.copy()
			motswap[j] = i
			motswapjoin = ''.join(motswap)
			if(motExiste(motswapjoin,dic) and motswapjoin != mot):
				l.append(motswapjoin)
	return l


dic=getDictionnaire()
a=input("Entrez un mot : ")
lmot=existSwapAllLetter(a.lower(),dic)
print(lmot)