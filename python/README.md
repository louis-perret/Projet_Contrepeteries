# Contrepèterie : l'Art de dé**c**aler les **s**ons !
* * *
### Application python sur console permettant la recherche de contrepèteries dans un mot et dans une phrase

* * *
* * *
<h1><u>Guide de lancement</u></h1>

```python
pip3 install -r requirements.txt #permet de télécharger le fichier requirements.txt
```
*requirements.txt* contient toutes les bibliothèques nécessaires au bon fonctionnement de l'application
Si jamais vous avez des problèmes de conflits entre des versions de python sur votre machine, lancer un environnement virtuel :
```python
pipenv shell
```
Cette dernière lancera l'environnement virtuel déjà crée à l'aide du fichier Pipfil.

Puis exécuter le fichier app_contrepeteries :
```python 
python3 app_contrepeteries
```
**Utiliser bien python3**, avec python2, l'application ne se lancera pas.
* * *

<h1><u>Explication</u></h1>

Au lancement de l'application, vous pouvez choisir la langue. A l'heure actuelle seules le français et l'anglais sont disponibles.

Ensuite vous avez le choix entre 2 modes :
```python
Sélectionnez le mode que vous souhaitez : 

a. Recherche de contrepèteries dans un mot
z. Recherche de contrepèteries dans une phrase
e. Configuration des filtres
r. Quitter
```

- Recherche dans les mots -> Permet de trouver des mots qui sont contrepets de celui entré par l'utilisateur
- Recherche dans une phrase -> Permet de trouver des contrepèteries au sein d'une phrase
- Configuration filtre -> Permet de modifier sa configuration actuelle

Vous trouverez des exemples d'utilisations tout le long de l'application afin de ne pas vous y perdre. Si vous souhaitez savoir comment elle a été réalisée, [lisez notre rapport](https://gitlab.iut-clermont.uca.fr/juduteyrat/contrepetries-regroupees/-/blob/master/documentation/Rapport_Projet_Contrep%C3%A8teries.pdf).