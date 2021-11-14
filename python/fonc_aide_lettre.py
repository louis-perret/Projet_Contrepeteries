from arbin import *
from filtre import *
import string
import sys
import json
import re
import os


# ----------------------------------------------------------------------------
"""
Remplace une lettre dans la chaine s à la position "index"
par la chaîne newstring.
i.e replacer("bonjour","pate",3) --> "bonpateour"
"""


def replacer(s, newstring, index,length):
	
	if index < 0:  # l'ajoute au début
		return newstring + s
	if index > len(s):  # l'ajoute à la fin
		return s + newstring
		# insère la nouvelle chaîne entre les tranches de l'original
	return s[:index] + newstring + s[index + length:]


"""
#temporaire, il faudra transformer remplacer en remplacer2 (avec param lenght en +) dans tout le code
def replacer2(s, newstring, index, lenght):

    if index < 0:  # l'ajoute au début
        return newstring + s
    if index > len(s):  # l'ajoute à la fin
        return s + newstring
    # insère la nouvelle chaîne entre les tranches de l'originalnsert the new string between "slices" of the original
    return s[:index] + newstring + s[index + lenght:]
"""

# ----------------------------------------------------------------------------
"""
Recherche dans le mot donné les mots possible en substituant une lettre
ex : model -> monel,motel,modal,modem,etc
retourne une liste de tuples des possibilitées au format :
[(mot,Anciennelettre,nouvellelettre),...]
"""


def aideLettreSubs(mot):

    listeDeMotCop = []
    compteur = 0
    print("Voici donc les lettres que l'on peut changer :")
    # pour chaque lettre du mot
    for lettre1 in enumerate(mot): #enumerate renvoie deux paramètres : la position de l'index et la valeur qui correspond

        print(f"  '{lettre1[1]}'", end='')
        # on regarde toutes les lettres possibles
        for lettre2 in list(string.ascii_lowercase): #pour chaque lettre de l'alphabet
            compteur += 1
            # si on remplace à l'index la lettre1 par lettre2,
            # et que ça forme un mot dans lexique, on ajoute le nvMot à la liste.
            nvMot = replacer(mot, lettre2, lettre1[0],1)

            test = isInDico('word', nvMot)

            if lettre1[1] != lettre2 and test: #Si on pas changé la lettre par elle même et si le mot existe
                listeDeMotCop.append((nvMot, lettre1[1], lettre2))
    print("\n")
    return listeDeMotCop



# ----------------------------------------------------------------------------
"""
Fonction temporaire visant à effectuer une contrepétrie en échangeant 2 lettres contre 1 lettre
"""


def aide2Lettre1Lettre(mot):

    listeDeMotCop = []
    print("Voici donc les lettres que l'on peut changer :")
    # pour chaque lettre du mot
    for lettre1 in enumerate(mot):

        if lettre1[0] == (len(mot)-1):
            break
                          

        doublelettre = lettre1[1]+mot[lettre1[0]+1]
        print(f"  '{doublelettre}'", end='')

        # on regarde toutes les lettres possibles
        for lettre2 in list(string.ascii_lowercase):
            # si on remplace à l'index les doubles lettres par lettre2,
            # et que ça forme un mot dans lexique, on ajoute le nvMot à la liste.
            nvMot = replacer(mot, lettre2, lettre1[0], 2) #On remplace 2 lettres par 1

            test = isInDico('word', nvMot)

            if test:
                listeDeMotCop.append((nvMot, doublelettre, lettre2))
    print('\n')
    return listeDeMotCop

# ----------------------------------------------------------------------------
"""
Fonction temporaire visant à effectuer une contrepétrie en échangeant 1 lettre contre 2 lettres
"""

def aide1Lettre2Lettre(mot):
	
	listeDeMotCop = []
	print("Voici donc les lettres que l'on peut changer :")
	# pour chaque lettre du mot
	for lettre1 in enumerate(mot):
		print(f"  '{lettre1[1]}'", end='')
		# on regarde toutes les lettres possibles
		for lettre2 in list(string.ascii_lowercase):
			#pour faire des couples
			for lettre3 in list(string.ascii_lowercase):
				# si on remplace à l'index de la lettre1 par lettre2+lettre3,
				# et que ça forme un mot dans lexique, on ajoute le nvMot à la liste.
				nvMot = replacer(mot, lettre2+lettre3, lettre1[0], 1) #On remplace 1 lettres par 2
				if isInDico('word', nvMot):
					listeDeMotCop.append((nvMot, lettre1[1], lettre2+lettre3))
	print('\n')
	return listeDeMotCop           		


# ----------------------------------------------------------------------------
"""
Gènère les quadruplets de l'aide, avec l'échange d'une seule lettre entre les mots.
Prend en argument la sortie de aideSonSub et l'index du mot saisie par l'utilisateur

retourne une liste de tuple de format :
(lettre1,lettre2,mot1',mot2',mot2)
lettre1 -> lettre saisie, que l'on désir échanger
lettre2 -> lettre selectionnée ensuite que l'on veut échanger avec lettre1

mot2 -> obtenu en échangeant lettre1 par lettre2 dans le mot d'origine

mot1'-> mot contenant lettre1
mot2'-> mot contenant lettre2
"""

def aideLettreRechDico(index, listeDeMotCop):
    index -= 1
    NombreDeMot = len(listeDeMotCop)
    compteur = 0
    listeDeMotNONCop = []
    listeDeRacines = []
    listeAffichage = []
    # config filtres
    with open('data/config.json') as diconfig_:
        diconfig = json.load(diconfig_)

    tsv_file = open("data/Lexique383.tsv", encoding="utf-8")
    lignes = csv.reader(tsv_file, delimiter="\t")
    # lit ligne par ligne du DICO (près de 100k lignes)
    # changer filtres
    diconfig = changerfiltre(diconfig)
    # bd filtres
    with open('data/DicoVulgaire.json') as vulgaire:
        BDvulgaire = json.load(vulgaire)

    for mot in lignes:
        mot = mot[0] #On recupère le mot qu'on veut tester

        for ChaqueLettre in range(len(listeDeMotCop)):

            test1 = listeDeMotCop[ChaqueLettre][2] in mot #Si la nouvelle lettre du mot listeDeMotCop[ChaqueLettre][2] est dans le mot du dictionnaire
            test2 = mot[:5] not in listeDeRacines
            # Racines:
            if index == ChaqueLettre and test1 and test2: #Si numéro du mot qu'on a sélectionné = index ChaqueLettre
            	#print(f" '{listeDeMotCop[ChaqueLettre][1]}' ")
                testDansMot = replacer(mot, listeDeMotCop[ChaqueLettre][1],
                                       mot.index(
                    listeDeMotCop[ChaqueLettre][2]),1) #replacer dans mot, à partir de l'index de là où se situe la nouvelle lettre par l'ancienne lettre
                # la lettre est dans le mot
                if isInDico('word', testDansMot):
                    # test we need
                    if diconfig["FiltreGrossier"] == "Oui":

                        if (listeDeMotCop[ChaqueLettre][0] in BDvulgaire or testDansMot in BDvulgaire or mot in BDvulgaire): #mot de base grossié, mot trouvé grossié ou mot du dico grossié
                            listeDeRacines.append(mot[:5])

                            listeAffichage.append((listeDeMotCop[ChaqueLettre][1],
                                                   listeDeMotCop[ChaqueLettre][2],
                                                   listeDeMotCop[ChaqueLettre][0],
                                                   testDansMot, mot))

                    else:
                        listeDeRacines.append(mot[:5])

                        listeAffichage.append((listeDeMotCop[ChaqueLettre][1],
                                               listeDeMotCop[ChaqueLettre][2],
                                               listeDeMotCop[ChaqueLettre][0],
                                               testDansMot, mot))
                    compteur += 1
    return (listeAffichage, compteur, diconfig)


# ----------------------------------------------------------------------------
"""
pretty print des resultats de l'aide sur les lettres et les syllabes.
"""


def affiRechLettre(listeAffichage, compteur, mot_origine):

    listeAffichage = (sorted(listeAffichage, key=lambda lettre: lettre[0])) #key = fonction qui prend lettre en param et ressort lettre[0] -> la liste sera trié par rapport à ça
    clear()

    while(True):
        compt = 1

        for pack in listeAffichage: #pack = (lettre1,lettre2,mot1',mot2',mot2)

            marge = len(str(compt))+2
            print(marge*" "+f"{mot_origine} - {pack[4]}")
            print(compt)
            print(marge*" "+f"{pack[2]} - {pack[3]}")
            print("\n"+"-"*30+"\n")
            compt += 1

        print(f"Nombre de combinaisons : {compt-1}")

        selecteur = None
        boucle = True
        while(boucle):
            try:
                selecteur = int(input(
                    "\n0 = quitter l'aide,-1 revenir au début de l'aide :\n"))
            except:
                print("\nVous n'avez pas saisi un chiffre")
                continue

            if selecteur == 0:
                return 0
            elif selecteur == -1:
                clear()
                return 1

            else:
                print("\nL'entrée n'est pas valide, réessayez")


"""
# ----------------------------------------------------------------------------
# Partie sur les syllabes :
# ----------------------------------------------------------------------------
"""
"""
Retourne un dico dont les clefs sont toutes les tranches du mots plus grandes
que tailleMin
"""

def tranchesMot(mot, tSlice):

    dicoSliceCom = {}
    for i in range(len(mot)):
        for j in range(i+1, len(mot)+1):
            if mot[i:j] != mot and j-i <= tSlice: #Pas plus de 3 lettres
                dicoSliceCom[mot[i:j]] = []

    return dicoSliceCom
# ----------------------------------------------------------------------------
"""
génère un itérateur de tuples contenant (debutMot,finMot) autour de toutes
les différentes tranches possible du mot.
"""
def DebFinMot(mot, tSlice):

    for i in range(len(mot)):
        for j in range(i+1, len(mot)+1):
            if mot[i:j] != mot and j-i <= tSlice:
                yield (mot[:i], mot[j:]) #retourne un générateur (itérateur qu'on ne parcours qu'une fois)


# ----------------------------------------------------------------------------
"""
Prend en argument le mot dont on veut les contrepétries,
La fonction retourne un dictionnaire avec en clefs la slice et en valeur
un ensemble contenant les mots contenant cette slice du mot d'origine
"""


def aideSyllSubs(mot_origine):

    tsv_file = open("data/Lexique383.tsv", encoding="utf-8")
    Lexlignes = csv.reader(tsv_file, delimiter="\t")

    with open('data/DicoVulgaire.json') as vulgaire:
        BDvulgaire = json.load(vulgaire)

    dicoSliceCom = tranchesMot(mot_origine, 3)


# recherche dans le lexique la correspondance des slices
    for ligne in Lexlignes:
        # on ne fait pas de recherche sur les mots composés et on exclue le mot d'entrée
        if '-' not in ligne[0] and ' ' not in ligne[0] and ligne[0] != mot_origine:
            ensTmp = []
            LexMot = ligne[0] #=mot qu'on teste du dico Lexique383

            iterDebFin = DebFinMot(mot_origine, 3)
# pour chaque tranche on recherche les mots dans lexique qui commencent
# et finissent de la même façon que le mot_origine:
# ex. danse -> slice: "an", on cherche les mots commençant
# par "d" et finissant par "se".

            for slice in dicoSliceCom.keys():
                try:
                    deb, fin = next(iterDebFin) #prend la valeur suivante de l'itérateur
                except:
                    break

                test = (len(LexMot) - len(deb) - len(fin)) <= 5
                if LexMot.startswith(deb) and LexMot.endswith(fin) and test: #si le mot commence et se termine par ce qu'on veut
                    dicoSliceCom[slice].append(LexMot)
    # on supprime les tranches qui n'ont pas de résultats
    dicoTmp = {}
    for i in dicoSliceCom.keys():
        if dicoSliceCom[i] != []:
            dicoTmp[i] = dicoSliceCom[i]

    print(f"Mot saisie : {mot_origine}")
    return dicoSliceCom


# -----------------------------------------------------------------------------
"""
Affichage intermédaire avant la fin.
Affiche les différentes tranches du mot d'origine qui peuvent êtres remplacées
pour former un mot dans le lexique
Retourne la tranche que souhaite échangé l'utilisateur dans le mot d'origine
"""


def affiNbCorrTranche(dicoSliceCom):
    # affichage du nombre de correspondances par slices
    index = 1
    for i in dicoSliceCom.keys():
        # elimination des doublons dans les listes.
        dicoSliceCom[i] = sorted(list(set(dicoSliceCom[i]))) #le set enlève les doublons, on convertit une liste ordonnée
        tailleString = 15 - len(str(i) + str(len(dicoSliceCom[i]))) #pour aligner dans l'affichage

        print(index, i, "-"*tailleString+">", len(dicoSliceCom[i]), "mots")
        index += 1

    print("\n0 : quitter l'aide/ -1 revenir au début de l'aide")
    selectSlice = None
    test = True
    while(test):
        try:
            selectSlice = int(
                input("Quelle partie voulez-vous voulez-vous échanger ? (rentrez leur indice) :"))
        except:
            print("")
        if selectSlice in range(1, len(dicoSliceCom.keys())+1):
            test = False
        elif selectSlice == 0:
            return 0
        elif selectSlice == -1:
            return -1
        else:
            print("L'entrée n'est pas valide, réessayez\n")
    return list(dicoSliceCom.keys())[selectSlice-1] #Récupère la liste des mots d'après l'échange selectionné


# -----------------------------------------------------------------------------
"""
Suite de affiNbCorrTranche,
affiche page par page de 60 mots des mot possibles en échangeant la tranches
rentrée par l'utilisateur dans la fonction précédante,
Retourne le mot selectionné par l'utilisateur qui l'intéresse pour l'echange
"""


def affiPageParPage(listeMot, syllOrigine, mot_origine):
    nbMotPage = 60  # nombre de mots par pages
    nbPage = (len(listeMot)//nbMotPage)  # nombre total de pages.
    numPage = 0                          # numéro page en cours

    tailleLigne = 50
    choix = {-1, -2}
    selecteur = 0
    continuer = True
    while(continuer):
        if selecteur == -2:
            numPage = numPage+1 if numPage+1 <= nbPage else numPage #Dépasse pas le nb page max
        elif selecteur == -1:
            numPage = numPage-1 if numPage-1 >= 0 else numPage #Pas en dessous 0 pages

        clear()
        print(f"page {numPage}/{nbPage}\n")

        for i in range(1, nbMotPage, 2): #de 1 à 60 avec un pas de 2

            mot1 = listeMot[nbMotPage*numPage+i-1] if nbMotPage*numPage+i-1 < len(listeMot) else ""
            mot2 = listeMot[nbMotPage*numPage+i] if nbMotPage*numPage+i < len(listeMot) else ""

            # recupération de la taille des mots pour l'espace entre les deux
            # c'est un pretty print
            tailleEspace = tailleLigne-len(mot1)

            if i <= 10:
                print(f"{i}  {mot1}", " "*tailleEspace, f"{i+1}  {mot2}")
            else:
                print(i, mot1, " "*tailleEspace, i+1, mot2)

        print(
            f"\nLes mots obtenables en remplaçant '{syllOrigine}' dans '{mot_origine}'")
        test = True
        while(test):

            try:
                selecteur = int(input("""
(0 : quitter l'aide/-3: revenir à selection précèdante /-4: revenir au début de l'aide)
(-1:Gauche / -2:Droite) ou saisissez numéro du mot :\n"""))
            except:
                print("\nVous n'avez pas saisi un chiffre")
                continue

            test1 = (nbMotPage*numPage+selecteur) <= len(listeMot) and (nbMotPage*numPage+selecteur) > 0 #Si je peux toujours afficher des mots

            if selecteur == 0:
                return 0
            elif selecteur == -3:
                clear()
                print(f"{mot_origine}\n")
                return True
            elif selecteur == -4:
                return -1
            elif selecteur in choix or test1:
                test = False
            else:
                print("\nL'entrée n'est pas valide, réessayez")
        continuer = False if selecteur not in choix else True
    return listeMot[nbMotPage*numPage+selecteur-1] #retourne le mot sélectionné par l'utilisateur pour l'échange


# ----------------------------------------------------------------------------
"""
Fait la liste des quaduplets d'échanges possibles:
de forme exemple :

(syll1,syll2,mot1',mot2',mot2)
"""

def aideSyllRechDico(mot_origine, selectMot, syllOrigine):
    		     # d'an'se      d'ar'se    an

    listeAffichage = []
    listeTmp = []

    # recup deb et fin de mot_origine:
    debFin = mot_origine.split(syllOrigine) #séparent le mot avec la syllabe choisie
    # extraction de 'ar' de selectMot.
    if len(debFin[1]) > 0: #Si la longueur de la fin du mot > 0
        syllNvlle = selectMot[len(debFin[0]):-len(debFin[1])] #on récupère juste 'ar' dans 'darse'

    else:
        syllNvlle = selectMot[len(debFin[0]):] #on récupère juste 'ar' dans 'darse'
    print(syllNvlle,"-",syllOrigine)
    tsv_file = open("data/Lexique383.tsv", encoding="utf-8")
    LexLignes = csv.reader(tsv_file, delimiter="\t")

    with open('data/DicoVulgaire.json') as vulgaire:
        BDvulgaire = json.load(vulgaire)

    with open('data/config.json') as diconfig_:
        diconfig = json.load(diconfig_)

    # lit ligne par ligne du DICO (près de 100k lignes)
    # changer filtres
    print('Maintenant il reste à gérer les filtres pour la génération')
    diconfig = changerfiltre(diconfig)

    for ligne in LexLignes:
        LexMot = ligne[0] #On récupère le mot du dico

        # cherche occurences de la nouvelle tranche dans le lexique
        if syllNvlle in LexMot:

            # on recupère le deb et fin du mot du lexique
            indexSyllNvlle = re.finditer(syllNvlle, LexMot) #retourne un itérateur
            indexSyllNvlle = [match.start() for match in indexSyllNvlle] 

            for i in indexSyllNvlle:
                # À partir de celles-ci on recupère le début et la fin de ce mot
                LexDeb = LexMot[:i]
                LexFin = LexMot[i+len(syllNvlle):]

                # on teste si le la concaténation du debut et fin de ce mot avec la slice
                # d'origine forment un mot qui existe dans le lexique
                testMot = LexDeb + syllOrigine + LexFin
                if isInDico('word', testMot) and testMot not in listeTmp:
                    if diconfig["FiltreGrossier"] == "Oui":
                        if (selectMot in BDvulgaire or testMot in BDvulgaire or LexMot in BDvulgaire):
                            listeAffichage.append([syllOrigine, syllNvlle,
                                                   selectMot, testMot,
                                                   LexMot])
                            listeTmp.append(testMot)
                    else:

                        # si oui on l'ajoute a notre liste de résultat.
                        listeAffichage.append([syllOrigine, syllNvlle,
                                               selectMot, testMot,
                                               LexMot])
                        listeTmp.append(testMot)
    return (listeAffichage, len(listeAffichage), diconfig)