from arbin import *
from filtre import *


def aideSonSubs(mot_origine,x,y):

    with open('data/dicoPhoncom.json') as tmp:
        dicoPhon = json.load(tmp)

    phon_file = open("data/BD_phoneme.txt", encoding="utf-8")
    BD_phoneme = phon_file.read()
    BD_phoneme = BD_phoneme.split("\n")
    del BD_phoneme[-1]
    listeDeMotCop = []
    
    mot = Mot_to_Phon_Only(arbre_mot, mot_origine)
    if not isinstance(mot, str):
	return 0
    clear()

    print(f"\nEn phonétique '{mot_origine}' se lit '{mot}'\n")

    listeCouple=recupCoupleLettre(y,"",[],BD_phoneme)
    print("Voici donc les sons que l'on peut changer :")
    for lettre1 in enumerate(mot):
        print(f"  '{lettre1[1]}'    ", end='')
	coupleLettre=recupCouple(mot,x,lettre[1])
	print(coupleLettre)
	if coupleLettre[0]:
		for couple in listeCouple:
		    # si on remplace à l'index la lettre1 par lettre2,
		    # et que ça forme un mot dans lexique, on ajoute le nvMot à la liste.
		    nvMot = replacer(mot, lettre2, lettre1[0],x)
		    test = isInDico('phon', nvMot)

		    if coupleLettre[1] != couple and test:
		    	listeDeMotCop.append((nvMot, lettre1[1], lettre2, dicoPhon[nvMot][0]))
    print("\n")
    return listeDeMotCop
