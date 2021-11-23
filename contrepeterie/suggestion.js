var dic=[];
var dicMot=[];
var dicPhon=[];
var affichResultat=[];

//const orange = '#FFA600';
//const green = '#28a745';

function handleFileSelect(evt) {
	
    var file = evt.target.files[0];
    Papa.parse(file, {
      header: true,
      dynamicTyping: true,
      complete: function(results) {
      	dic.push(results);
      	console.log(dic);
      	splitdicSelector()
      }
    });
    
    //console.log(dicMot);
    //console.log(dicPhon);
    
  }

  $(document).ready(function(){
$("#csv-file").change(handleFileSelect);
});

  function splitdicSelector(){
	for(let i=0; i<dic[0]['data'].length; i++){
  		dicMot.push(dic[0]['data'][i][0]);
		dicPhon.push(dic[0]['data'][i][1]);	
  	}
  	console.log("Affichage du dctionaire de mots");
  	console.log(dicMot);
  	console.log("Affichage du dctionaire de sons");
  	console.log(dicPhon);
}

function load(){
	document.getElementById('chargement').innerHTML = 'Dictionnaire en cours de chargement';
	document.getElementById('chargement').style.backgroundColor=orange;

	Papa.parse(pathToDictionnary, {
    download: true,
    step: function(row) {
    	dic.push(row);
      	
    },
    complete: function() {
    	document.getElementById('chargement').innerHTML = 'Dictionnaire chargé';
		document.getElementById('chargement').style.backgroundColor=green;
		document.getElementById('genener').disabled=true;
        console.log("All done!");
        console.log(dic);
        console.log("Appel de split dic");
        splitdic(dic);

    }
  });
}

function splitdic(){
    for(let i=0; i<dic.length; i++){
  		dicMot.push(dic[i]['data'][0]);
		dicPhon.push(dic[i]['data'][1]);	
  	}
  	console.log("Affichage du dictionaire de mots");
  	console.log(dicMot);
  	console.log("Affichage du dictionaire de sons");
  	console.log(dicPhon);
}


function motExiste(mot, dic){
	if(dic.includes(mot))
		return true;
	return false;
}



//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
/*
//Fonction qui remplace a un index donné, une lettre donnée.
String.prototype.replaceAt = function(index, replacement) {
	if (index >= this.length) {
		return this.valueOf();
	}

	var chars = this.split('');
	chars[index] = replacement;
	return chars.join('');
}
*/


//redirige vers l'exécution de aideLettreSubs() ou aidePhonemeSubs() selon si
//l'utilisateur a sélectionné choixLettre ou choixPhoneme
function redirigeLettreOuPhoneme() {
	if (document.getElementById('choixLettre').value == 'true')
	{
		//aideLettreSubs();

		//servira pour plusieurs lettres/plusieurs lettres
		if (document.getElementById('choixDeX').value == "" || document.getElementById('choixDeY').value == "")
		{
			if (document.getElementById('choixDeX').value == "" && document.getElementById('choixDeY').value == "")
				aideMultiLettre(1, 1);
			else if (document.getElementById('choixDeX').value == "")
				aideMultiLettre(1, document.getElementById('choixDeY').value);
			else if(document.getElementById('choixDeY').textContent == "")
				aideMultiLettre(document.getElementById('choixDeX').value, 1);
        }
		else
			aideMultiLettre(document.getElementById('choixDeX').value, document.getElementById('choixDeY').value);
		
	}
	else
		aidePhonemeSubs();
}




/*
Objectif: Renvoie un couple de x lettre(s) à partir de l'index index dans le mot mot
Paramètres:
-Entrée :
mot: mot sur lequel on va récupérer le couple
x: nombre de lettres pour le couple
index: à partir de qu'elle lettre
	- Sortie :
Renvoie un tuple de la forme: boolean, couple.
*/
function recupCouple(mot, x, index) {
	//console.log("----------------------------------Valeur de mot :" +mot);
	//console.log("----------------------------------Valeur de x :" +x);
	//console.log("----------------------------------Valeur de index :" +index);
	if (x > 1) {
		//console.log("----------------------------------Valeur de index+1 :" + (index + 1));
		//console.log("----------------------------------Valeur de length :" + mot.length);
		if ((index + 1) === mot.length)
			return ['false', '']
		
		/* peut-être à remplacer par
		if ((index + (x - 1)) >= mot.length)
		return ['false', '']
		*/

	}
	//console.log("Je return : " + 'true' + ', ' +mot.substr(index, x))
	return ['true', mot.substr(index, x)];
}

/*
Objectif : Renvoie une liste des couples possibles de lettres à partir de l'alphabet
Paramètres :
	-Entrée :
		-y : nombre lettres pour la combinaison
		-a : chaîne contenant la combinaison (utile pour la récursivité, vide au premier appel)
		-liste : liste des réponses (utile pour la récursivité, vide au premier appel)
	-Sortie :
		-listeCouple : liste des réponses

Exemple : Si je désire récupérer tous les couples de 2 lettres possibiles à partir de l'alphabet, j'utilise cette fonction qui me retournera une liste qui contiendra : aa,ab,ac,ad,...,zz.
*/
function recupCoupleLettre(y, a, liste, alphabet) {
	listeCouple = liste;
	for (let i = 0; i < alphabet.length; i++)
		{
		var l = alphabet[i]
			if (y == 1)
				listeCouple.push(a + l);
			else
			listeCouple = recupCoupleLettre(y - 1, a + l , listeCouple,alphabet);
	}
	return listeCouple
}
/*
//Remplace une partie de mot par nvpartie, depuis indexDebut et pendant longueur charactères
function replaceBetween(mot, nvPartie, indexDebut, longueur) {
	console.log(mot.substring(0, indexDebut) + nvPartie + mot.substring(indexDebut, mot.lenght).substring(longueur, mot.lenght));// doit pouvoir être simplifié
};
*/
String.prototype.replacerAvecIndex = function (index, x, string) {
	if (index < 0)
		return string
	if (index > this.length)
		return this.substring(0) + string;
	return this.substring(0,index-(x-1)) + string + this.substring(index+1,this.length);
};

/////////////////////////////////////////////////////////////////////////////////////////////////


function updateBtn() {
	let mo = document.getElementById('mot').value;
	mot=mo.toLowerCase(); //On recuperer en minuscule le mot saisi au clavier
	console.log("mot :" + mot);

	var iButton = $(this).val();
	console.log("test click " + iButton);

	aideLettreRechDico(mot,iButton, document.getElementById("choixDeX").value, document.getElementById("choixDeY").value);
}


function choixMotCompatible(motSave,listeMotCompatible) {
	var element = document.getElementById("div1");
	while (element.firstChild){
		element.removeChild(element.firstChild);
	}

	for (var i = 0; i < listeMotCompatible.length; i++) {
			let button = document.createElement("button");
			button.innerText =motSave+" - " + listeMotCompatible[i];
			button.value =listeMotCompatible[i];
			document.getElementById("div1").append(button);
			button.addEventListener('click', updateBtn);

	}
}

//changement des valeurs des éléments choixLettre et choixPhoneme selon la sélection
function choixLettre() {
	if (document.getElementById('choixLettre').value == 'false')
	{
		document.getElementById('choixLettre').value = 'true';
		document.getElementById('choixPhoneme').value = 'false';
    }
}

function choixPhoneme() {
	if (document.getElementById('choixPhoneme').value == 'false')
	{
		document.getElementById('choixPhoneme').value = 'true';
		document.getElementById('choixLettre').value = 'false';
    }
}


/*
//Fonction qui va trouver 2 mots pour former le groupe des 4 mots
function chercheMotDico(lettre1,lettre2,x,y,resMot1,resMot2) {
	console.log("lettre 1 : " + lettre1);
	console.log("lettre : " + lettre2);
	for(let i=0;i<10000;i++){ //Pour chaque mots du dico
		let mot1=dicMot[i]; //On prend le premier mot
		
		console.log("motrecherché = "+mot1)
		console.log("poslettre1 :" +mot1.indexOf(lettre1));
		let posLettre1=mot1.indexOf(lettre1); //On regarde ou la lettre1 est dans ce mot

		if(posLettre1 != -1 && mot1.length<5) { //Si la lettre1 est presente dans le mot 1 du dico
			for(let j=0;j<dicMot.length;j++){ //Pour chaque mot du dico
				let mot2=dicMot[j]; //On prend le premier mot
				if (mot1.length == mot2.length && mot1 != mot2 ) { //Si les 2 mots sont de meme longueur et ne sont pas les memes
					var lettreCommune = 0;
					for (let k=0;k<mot1.length;k++) { //Pour chaque lettre du mot1

						if (mot1[k] == mot2[k]){ //Si la lettre au meme index entre les 2 mots est identique :
							lettreCommune++; //On incremente cette variable
						}
					}
					var posLettre2=mot2.indexOf(lettre2);//On regarde ou la lettre1 est dans ce mot
					if(posLettre2 != -1) { //Si la lettre2 est presente dans le mot 2 du dico
						if (posLettre1 == posLettre2 && lettreCommune == mot1.length-1 ) { //On regarde si les deux mots ont la lettre1 et la lettre2 au meme endroit
							resMot1.push(mot1); //Et on regarde si le mot2 a toutes ses autres lettres differentes du mot grace a "LettreCommune"
							resMot2.push(mot2);//Si c'est le cas on ajoute les 2 mots dans les tableaux respectifs
							console.log("trouve");
							break;
						}
					}
				}

			}
		}
	}
	console.log("Mot 1 : " + resMot1);
	console.log("mot 2 : " + resMot2);
}
*/

function chercheMotDico(lettre1,lettre2,x,y,resMot1,resMot2) {
	var diffXY = x - y;
	console.log("diffXY : " + diffXY);
	console.log("lettre 1 : " + lettre1);
	console.log("lettre 2 : " + lettre2);
	for(let i=0;i<dicMot.length;i++){ //Pour chaque mots du dico
		let mot1=dicMot[i]; //On prend le premier mot
		lg1=mot1.length;
		longueur1=lg1-diffXY;
		let posLettre1=mot1.indexOf(lettre1); //On regarde ou la lettre1 est dans ce mot

		if(posLettre1 != -1 && mot1.length<5) { //Si la lettre1 est presente dans le mot 1 du dico
			for(let j=0;j<dicMot.length;j++){ //Pour chaque mot du dico
				let mot2=dicMot[j]; //On prend le premier mot
				lg2=mot2.length;
				longueur2=lg2-diffXY;

				if (diffXY ==0 ) { //MARCHE OK !!!!!!
					//Rentre ici : testé
					if (mot1.length == mot2.length && mot1 != mot2) { //Si les 2 mots sont de meme longueur et ne sont pas les memes
						var lettreCommune = 0;
						for (let k=0;k<mot1.length;k++) { //Pour chaque lettre du mot1

							if (mot1[k] == mot2[k]){ //Si la lettre au meme index entre les 2 mots est identique :
								lettreCommune++; //On incremente cette variable
							}
						}
						var posLettre2=mot2.indexOf(lettre2);//On regarde ou la lettre1 est dans ce mot
						if(posLettre2 != -1) { //Si la lettre2 est presente dans le mot 2 du dico
							if (posLettre1 == posLettre2 && lettreCommune == mot1.length-1 ) { //On regarde si les deux mots ont la lettre1 et la lettre2 au meme endroit
								resMot1.push(mot1); //Et on regarde si le mot2 a toutes ses autres lettres differentes du mot grace a "LettreCommune"
								resMot2.push(mot2);//Si c'est le cas on ajoute les 2 mots dans les tableaux respectifs
								console.log("trouve");
								break;
							}
						}
					}
				}
				if (diffXY > 0 ) { //FONCTIONNEL NORMALEMENT MAIS A TESTER
					//Rentre ici : testé
					if (longueur1 == mot2.length) { //Si le premier mot fait x lettres et le deuxieme fait x-1 lettres
						var lettreCommune = 0;
						console.log("mot 1 ex  : " + mot1);
						console.log("mot 2 ex : " + mot2);
						var posLettre2=mot2.indexOf(lettre2);//On regarde ou la lettre1 est dans ce mot
						if(posLettre2 != -1 && posLettre1 == posLettre2) {
							mot1test=mot1.replace(lettre1,"")
							mot2test=mot2.replace(lettre2,"")
							console.log("tets !!!!! : " + mot1test)
							console.log("tets !!!!! : " + mot2test)
							for (let k=0;k<mot1test.length;k++) { //Pour chaque lettre du mot1

								if (mot1test[k] == mot2test[k]){ //Si la lettre au meme index entre les 2 mots est identique :
									lettreCommune++; //On incremente cette variable
								}
							}
							console.log("Nb lettres communes : " + lettreCommune)
								if (lettreCommune == longueur2) { //On regarde si les deux mots ont la lettre1 et la lettre2 au meme endroit
									resMot1.push(mot1); //Et on regarde si le mot2 a toutes ses autres lettres differentes du mot grace a "LettreCommune"
									resMot2.push(mot2);//Si c'est le cas on ajoute les 2 mots dans les tableaux respectifs
									console.log("trouve");
									break;
								}
						}
					}
				}
				if (diffXY < 0 ) {
					//Rentre ici : testé
					if (longueur1 == mot2.length) { //Si le premier mot fait x lettres et le deuxieme fait x-1 lettres
						var lettreCommune = 0;
						var posLettre2=mot2.indexOf(lettre2);//On regarde ou la lettre1 est dans ce mot
						if(posLettre2 != -1 && posLettre1 == posLettre2) {
							mot1test=mot1.replace(lettre1,"")
							mot2test=mot2.replace(lettre2,"")
							console.log("mot 1 ex  : " + mot1);
							console.log("mot 2 ex : " + mot2);
							console.log("tets !!!!! : " + mot1test)
							console.log("tets !!!!! : " + mot2test)
							for (let k=0;k<mot1test.length;k++) { //Pour chaque lettre du mot1

								if (mot1test[k] == mot2test[k]){ //Si la lettre au meme index entre les 2 mots est identique :
									lettreCommune++; //On incremente cette variable
								}
							}
							console.log("Nb lettres communes : " + lettreCommune)
							if (lettreCommune == longueur2) { //On regarde si les deux mots ont la lettre1 et la lettre2 au meme endroit
								resMot1.push(mot1); //Et on regarde si le mot2 a toutes ses autres lettres differentes du mot grace a "LettreCommune"
								resMot2.push(mot2);//Si c'est le cas on ajoute les 2 mots dans les tableaux respectifs
								console.log("trouve");
								break;
							}
						}
					}
				}



				/*switch(diffXY) {
					case diffXY > 0:
						if (mot1.length == mot2.length-diffXY) { //Si les 2 mots ne sont pas les memes
							var lettreCommune = 0;
							for (let k=0;k<mot1.length;k++) { //Pour chaque lettre du mot1

								if (mot1[k] == mot2[k]){ //Si la lettre au meme index entre les 2 mots est identique :
									lettreCommune++; //On incremente cette variable
								}
							}
							var posLettre2=mot2.indexOf(lettre2);//On regarde ou la lettre1 est dans ce mot
							if(posLettre2 != -1) { //Si la lettre2 est presente dans le mot 2 du dico
								if (posLettre1 == posLettre2 && lettreCommune == mot1.length-1 ) { //On regarde si les deux mots ont la lettre1 et la lettre2 au meme endroit
									resMot1.push(mot1); //Et on regarde si le mot2 a toutes ses autres lettres differentes du mot grace a "LettreCommune"
									resMot2.push(mot2);//Si c'est le cas on ajoute les 2 mots dans les tableaux respectifs
									console.log("trouve");
									break;
								}
							}
						}
						break;

					case diffXY < 0:
						console.log("??????????????????????????")
						if (mot1.length == mot2.length+diffXY) { //Si les 2 mots ne sont pas les memes
							var lettreCommune = 0;
							for (let k=0;k<mot1.length;k++) { //Pour chaque lettre du mot1

								if (mot1[k] == mot2[k]){ //Si la lettre au meme index entre les 2 mots est identique :
									lettreCommune++; //On incremente cette variable
								}
							}
							var posLettre2=mot2.indexOf(lettre2);//On regarde ou la lettre1 est dans ce mot
							if(posLettre2 != -1) { //Si la lettre2 est presente dans le mot 2 du dico
								if (posLettre1 == posLettre2 && lettreCommune == mot1.length-1 ) { //On regarde si les deux mots ont la lettre1 et la lettre2 au meme endroit
									resMot1.push(mot1); //Et on regarde si le mot2 a toutes ses autres lettres differentes du mot grace a "LettreCommune"
									resMot2.push(mot2);//Si c'est le cas on ajoute les 2 mots dans les tableaux respectifs
									console.log("trouve");
									break;
								}
							}
						}
						break;

					default :
						console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
						if (mot1.length == mot2.length && mot1 != mot2) { //Si les 2 mots sont de meme longueur et ne sont pas les memes
							var lettreCommune = 0;
							for (let k=0;k<mot1.length;k++) { //Pour chaque lettre du mot1

								if (mot1[k] == mot2[k]){ //Si la lettre au meme index entre les 2 mots est identique :
									lettreCommune++; //On incremente cette variable
								}
							}
							var posLettre2=mot2.indexOf(lettre2);//On regarde ou la lettre1 est dans ce mot
							if(posLettre2 != -1) { //Si la lettre2 est presente dans le mot 2 du dico
								if (posLettre1 == posLettre2 && lettreCommune == mot1.length-1 ) { //On regarde si les deux mots ont la lettre1 et la lettre2 au meme endroit
									resMot1.push(mot1); //Et on regarde si le mot2 a toutes ses autres lettres differentes du mot grace a "LettreCommune"
									resMot2.push(mot2);//Si c'est le cas on ajoute les 2 mots dans les tableaux respectifs
									console.log("trouve");
									break;
								}
							}
						}
				}*/
			}
		}
	}
	console.log("Mot 1 : " + resMot1);
	console.log("mot 2 : " + resMot2);
}

//Fonction qui va trouver la difference de lettre entre deux mots
function aideLettreRechDico(mot1, mot2, x, y) {
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
	var resMot1=[]; //on crée 2 tableaux pour accueuillir tous les mots qui vont etre trouvés
	var resMot2=[];
	console.log("!!!!!!!!!!lettremot1 : "+lettreMot1)
	console.log("!!!!!!!!!!!lettremot2 : "+lettreMot2)
	chercheMotDico(lettreMot1,lettreMot2,saveX,saveY,resMot1,resMot2);//fonction pour trouver les 4 mots
	for (let j = 0; j <resMot1.length ; j++) { //Pour chaque mot de resMot1
		affichResultat.push('<b>' + mot1 + '</b>&#9;' + ' - ' + resMot2[j] ); //On ajoute dans une variable globale
		affichResultat.push(mot2 + ' - ' + resMot1[j] );//Le mot saisi - le mot avec la lettre du mot2
		affichResultat.push('----------------');        //Le mot 2 (compatible) - le mot avec la lettre du mot1
	}
	affichageMot(affichResultat);
}




function affichageMot(l){
	var element = document.getElementById("div1");
	while (element.firstChild){
  		element.removeChild(element.firstChild);
	}
	for(var i=0; i<l.length; i++){
		let par = document.createElement('p');
		par.innerHTML=l[i];
		document.getElementById('div1').append(par);
	}
}
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------





