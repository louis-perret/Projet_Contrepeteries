


//vérifie si une contrepétrie est valide avec espaces
function verificationEspaces(mot, ancienneLettre, nouvelleLettre, index) {
	listeMot = []
	for (var l = 0; l < mot.length; l++) {
		if (l >= 2 && l <= mot.length - 2) {
			motEspace1 = mot.replacerAvecIndex(index, nouvelleLettre.length, nouvelleLettre+' ');
			motSplit = motEspace1.split(' ');

			if (motExiste(motSplit[0], dicMot) && motExiste(motSplit[1], dicMot) && !motExiste(motEspace1, listeMot)) {
				listeMot.push(motEspace1);
			}
		}
	}

	return listeMot;
}


//Fonction principale
//Fonction qui rend une liste de mot compatible -> pour code = gode, cote, iode...
//Va ensuite appeler les fonctions pour trouver les groupes de 4 mots
//Traduction de la fonction de généralisation python en JS
function aideMultiLettre(x, y) {

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
    if (document.getElementById("couperMots").checked) {
        //pour les mots coupés, mais ne marche pas -> seulement une lettre et un espace est échangée (pas 2 lettres et un espace par exemple, dans le cas x=2 y=1)
        for (let j = 0; j < alph.length; j++) { //Pour chaque lettre de l'alphabet {
            mot2 = mot2.replaceAt(i, alph[j]); //On remplace la lettre du mot par la lettre de l'alphabet
            var tabVerifEspaces = verificationEspaces(mot, mot[i], mot2[i], i);
            mot2temp = mot2.replace(" ", "");
            var lengthmot = mot.length
            lMot = lengthmot - (x - y);

            if (tabVerifEspaces != "" && lMot == mot2temp.length)
                l.push(tabVerifEspaces);
        }
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

			  nvtMot=nvtMot.replace(" ","");
			  console.log("Mot a tester : " + nvtMot)	
			  var lengthmot = mot.length
			  lMot=lengthmot-(x-y);
			  console.log("longueur mot saisi - diffxy = " + lMot);
			  
              if (nvtMot != mot && motExiste(nvtMot, dicMot) && lMot == nvtMot.length) { //Si le mot existe et si on n'a pas remplacé par les mêmes lettres
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



//Fonction qui va trouver la difference de lettres entre deux mots, essentiel pour permettre de trouver le groupe de 4 mots
function aideLettreRechDico(mot1, mot2) {
	document.getElementById('loadingStats').style.visibility = "collapse";
	document.getElementById("bRetour2").setAttribute("class","mt-3");
	document.getElementById("bRetour").setAttribute("class","mt-3");
	affichResultat=[]
	x=document.getElementById("choixDeX").value;
	y=document.getElementById("choixDeY").value;
	var lettreMot1 = "";
	var lettreMot2 = "";
	let saveX = x;
	let saveY = y;
	for (let i=0; i<mot1.length; i++) { //Pour chaque lettre du mot 1 (mot saisi)

		if (mot1[i] != mot2[i]) { //Si la lettre au meme indice n'est pas la meme sur les 2 mots
			let saveI = i;

			for(x; x>0; x--){
				lettreMot1 = lettreMot1 + mot1[i]; //On stock les lettres qui changent
				i++;
			}
			i = saveI;
			for(y; y>0; y--){
				lettreMot2 = lettreMot2 + mot2[i]; //On stock les lettres qui changent
				i++;
			}
			break;
		}
	}
	console.log("lettres1 " + lettreMot1)
	console.log("lettres2 " + lettreMot2)

	var resMot1=[]; //on crée 2 tableaux pour accueuillir tous les mots qui vont etre trouvés
	var resMot2=[];

	chercheMotDico(lettreMot1,lettreMot2,saveX,saveY,resMot1,resMot2);//fonction pour trouver les 4 mots
	document.getElementById("loadingStats").style.visibility="collapse";
	//On prepare l'affichage des 4 mots un à un
	for (let j = 0; j <resMot1.length ; j++) { //Pour chaque mot de resMot1
		if(mot1 != resMot1[j]) {
			//affichResultat.push("<div style ='margin: 10px;'><div class='card p-2 shadow-sm'>"+ dicMot[indexMotDic1] + ' - ' + dicMot[indexRes2] + '</div>' + '<div class="card p-2 shadow-sm">' + dicMot[indexMotDic2] + ' - ' + dicMot[indexRes1] +'</div></div>')
			affichResultat.push("<div style='margin: 10px;'><div class='card p-2 shadow-sm'>"+ mot1 + ' - ' + resMot2[j] + '</div>' + '<div class="card p-2 shadow-sm">' + mot2 + ' - ' + resMot1[j] +'</div></div>')
		}
	}
	affichageMot(affichResultat);
}