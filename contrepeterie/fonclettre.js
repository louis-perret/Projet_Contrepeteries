//Fonction principale
//Fonction qui rend une liste de mot compatible -> pour code = gode, cote, iode...
//Va ensuite appeler les fonctions pour trouver les groupes de 4 mots
function aideLettreSubs() {
	affichResultat=[];
	var l = [];
	let mot = document.getElementById('mot').value.toLowerCase(); //On recuperer en minuscule le mot saisi au clavier
	console.log("mot :" + mot);
	//console.log(dicMot);
	if (mot.length == 0)
		return;
	let ind = 0;
	for(let j=0;j<dicMot.length;j++){ //On trouve l'index de ce mot dans le dico
		if(dicMot[j] == mot){
			ind = j;
		}
	}
	if (ind==0) {
		l.push("Aucune correspondance");
		affichageMot(l);
		l=[];
		return;
	}
	var mot2=dicMot[ind]; //On copie ce mot dans mot2
	var alph=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
	let motSave=mot2; //On garde le mot en memoire

	for (let i=0; i<mot2.length; i++) { //Pour chaque lettre de notre mot
		mot2=motSave; //On reinitialise le mot ici afin d'avoir toujours "code" au lieu de "zode" puis "zzode" par ex
		for(let j=0;j<alph.length;j++) { //Pour chaque lettre de l'alphabet
			mot2 = mot2.replaceAt(i, alph[j]); //On remplace la lettre du mot par la lettre de l'alphabet

			var tabVerifEspaces = verificationEspaces(mot, mot[i], mot2[i], i);
			if (tabVerifEspaces != "")
				l.push(tabVerifEspaces);

			if (motExiste(mot2,dicMot) && mot2 != mot) { //Si le mot existe et que le mot n'est pas le mot saisi
				console.log('Ok : ' + mot2 + " ajouté");
				let iter = dicMot.indexOf(mot2);
				if(dicMot[iter] != mot){
					l.push(dicMot[iter]); //On ajoute le mot dans la liste l des mots compatibles
				}
			}
		}

	}
	console.log("liste mot compatible " + l);
	choixMotCompatible(motSave,l);
}

//vérifie si une contrepétrie est valide avec espaces
function verificationEspaces(mot, ancienneLettre, nouvelleLettre, index) {
	listeMot = []
	console.log("###"+ancienneLettre)
	console.log("'''" + nouvelleLettre)
	console.log("---" + index)

	for (var l = 0; l < mot.length; l++) {
		if (l >= 2 && l <= mot.length - 2) {
			motEspace1 = mot.replacerAvecIndex(index, nouvelleLettre.length, nouvelleLettre+' ');
			motSplit = motEspace1.split(' ');
			console.log("!!!!!!!!- motEspace1 : " + motEspace1)
			console.log("!!!!!!!!- motSplit : " + motSplit)
			console.log("!!!!!!!!- motSplit0 : " + motSplit[0])
			console.log("!!!!!!!!- motSplit1 : " + motSplit[1])
			if (motExiste(motSplit[0], dicMot) && motExiste(motSplit[1], dicMot) && !motExiste(motEspace1, listeMot)) {
				listeMot.push(motEspace1);
			}
		}
	}

	return listeMot;
}


//Prototype de la fonction principale, en enlevant x lettres du mot rensigné et y lettres du mot recherché
//Traduction de la fonction de généralisation python en JS
function aideMultiLettre(x, y) {
    bonjour="bonjour"
    bonjour=bonjour.replacerAvecIndex(3,"pate")
    console.log("Test replacer :" + bonjour)

  //replaceBetween(document.getElementById('mot').value, "ch", x, 2);
  affichResultat = [];
  var l = [];
  let mot = document.getElementById('mot').value.toLowerCase(); //On recuperer en minuscule le mot saisi au clavier
  if (mot.length == 0)
      return;
  let ind = 0;
  for (let j = 0; j < dicMot.length; j++) { //On trouve l'index de ce mot dans le dico
      if (dicMot[j] == mot) {
          ind = j;
      }
  }
  var mot2 = dicMot[ind]; //On copie ce mot dans mot2
  var alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
  let motSave = mot2; //On garde le mot en memoire
  let listeCouple = recupCoupleLettre(y, '', [], alph); //Récupère la liste de combinaisons possibles de longueur y
  console.log("Voici donc les lettres que l\'on peut changer :[ ");
  for (var i = 0; i < mot.length; i++) //Pour chaque lettre du mot
  {

	  //pour les mots coupés, mais ne marche pas -> seulement une lettre et un espace est échangée (pas 2 lettres et un espace par exemple, dans le cas x=2 y=1)
	  for (let j = 0; j < alph.length; j++) { //Pour chaque lettre de l'alphabet {
		  mot2 = mot2.replaceAt(i, alph[j]); //On remplace la lettre du mot par la lettre de l'alphabet

		  var tabVerifEspaces = verificationEspaces(mot, mot[i], mot2[i], i);
		  if (tabVerifEspaces != "")
			  l.push(tabVerifEspaces);
	  }

      var coupleLettre = recupCouple(mot, x, i); //on recupère le prochain couple de lettre à échanger //lettre[0] dans python = i ici normalement
      //console.log("true ou false ? : " + coupleLettre[0])
      if (coupleLettre[0] == 'true') //S'il existe un couple possible à échanger
      {
          console.log(coupleLettre[1] + " , ");
          for (j = 0; j < listeCouple.length; j++) //Pour chaque combinaison possible
          {
              couple = listeCouple[j]
              var nvtMot = mot.replacerAvecIndex(i, x, couple)
              console.log("NvMot = " + nvtMot)
              //var nvtMot = replaceBetween(mot, couple, i, x); //On remplace

              if (nvtMot != mot && motExiste(nvtMot, dicMot)) { //Si le mot existe et si on n'a pas remplacé par les mêmes lettres
                  console.log("++++++++++++++++++++++++++++++++++++Mot ajouté : " + nvtMot)
                  l.push(nvtMot);
              }

          }
      }
  }
  console.log(" ]")
  //console.log("--------------------------Ma liste compatible : " + l)
  choixMotCompatible(motSave, l);
  
}
