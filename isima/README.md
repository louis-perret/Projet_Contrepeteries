# Bienvenue dans ce projet de génération et d'aide à la contrepétrie.

### Pour lancer le projet il vous faudra lancer le fichier <span style="color:#D61313"> *input.py* </span> qui est celui qui va appeler tout les autres.

Pour lancer le projet il vous faudra avoir téléchargé les libairies suivantes :

Les natives :
  * json
  * os
  * re
  * sys
  * string
  * csv

À trouver :
  *  language_tool_python

**pip install --upgrade language_tool_python** *pour ceux sous ubuntu*

ou le lien de la page projet : https://pypi.org/project/language-tool-python/

### Aussi votre répertoire doit contenir les fichiers suivants :

* **input.py**
* echSyllabe.py
* aideContre.py
* fonc_aide_son.py
* fonc_aide_lettre.py
* filtre.py
* arbin.py

### Ainsi qu'un répertoire **data** contenant :

* config.json :

Contient la configuration de notre programme, modifiable par l'utilisateur

* BD_phoneme.txt :

Contient tout les caractères différents symbolisant les sons, les phonèmes

* Lexique383.tsv :

Contient tout les mots de la langue française, vulgaire, argo,etc, leur traduction phonétique, leur racine, leurs types grammaticaux, etc. (nous conseillons aux prochains de mieux exploiter que nous les différentes données que le fichier propose pour la réalisation de leurs filtres.)

* dicoPhoncom.json :

Contient un dictionnaire où chaque clefs est un mot écrit en phonétique et la valeur est une liste des mots ayant cette phonétique écrient dans différents orthographes (créé à partir du Lexique).

* DicoVulgaire.json:

Contient une liste de mots vulgaires de la langue française. Utilisée pour filtrer les résultats

### Finalement, vous devez avoir un fichier rapport.pdf :

Qui est notre rapport de projet et simili aide pour les prochains pizz (ou autre) qui tenteraient de récupérer nos fonctions pour ajouter des fonctionnalités.

Nous vous conseillons de bien suivre les cours de MRP pour les pizz, car ils pourront vous apporter des notions de pythons que nous avons sous/pas exploitées dans nos fonctions.

exemple : dans echSyllabe, les fonctions **'mixSyllabes'** pourraient être GRANDEMENT simplifiées et être passée en générateurs d'itérateurs pour simplifier les sorties et l'algorithmique de cette partie.

### Note pour la config de <span style="color:#D61313"> *clear()* </span>

Selon votre système d'exploitation, cette fonction peut "buguer",

Si la config du clear est en mode "effacer définitivement" alors ce bug consiste
en ne pas effacer le terminal et afficher un message d'erreur sans quitter le programme.

Ce cas de figure peut apparaître chez les OS types mac, windows, et autre ubuntu
(On n'avait pas ces OS sous la mains pour tester)
