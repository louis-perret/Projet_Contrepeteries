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
  	console.log("Affichage du dctionaire de mots");
  	console.log(dicMot);
  	console.log("Affichage du dctionaire de sons");
  	console.log(dicPhon);
}


function motExiste(mot, dic){
	if(dic.includes(mot))
		return true;
	return false;
}


//fonction permettant la contrepétrie à base de phonèmes, échange d'1 phonème contre 1 phonème
function aidePhonemeSubs(){
	affichResultat=[];
	var l=[];
	let mo = document.getElementById('mot').value;
	mot=mo.toLowerCase();
	console.log("mot :" + mot);
	if (mot.length == 0)
		return
	let ind = 0;
	for(let j=0;j<dicMot.length;j++){
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
	console.log("ind :" + ind);
	var mot2=dicPhon[ind];
	console.log("mot2 :" + mot2);
	var alph = ['b', 'd', 'f', 'g', 'k', 'l', 'm', 'n', 'ŋ','ɲ','p','ʁ','s', 'ʃ', 't', 'v', 'z', 'ʒ', 'j', 'w','ɥ', 'a', 'ɑ', 'e', 'ɛ','ɛː','ə','i', 'œ','ø','o','ɔ','u','y','ɑ̃','ɛ̃','œ̃','ɔ̃'];
	let motSave=mot2; //On garde le mot en memoire
	var m=mot2.split('');
	console.log(m);

	for (let i=0; i<mot2.length; i++) { //Pour chaque lettre de notre mot
		mot2=motSave; //On reinitialise le mot ici afin d'avoir toujours "code" au lieu de "zode" puis "zzode" par ex
		for(let j=0;j<alph.length;j++) { //Pour chaque lettre de l'alphabet
			mot2 = mot2.replaceAt(i,alph[j]); //On remplace la lettre du mot par la lettre de l'alphabet
			console.log(mot2);
			if (motExiste(mot2,dicPhon) && mot2 != mot) { //Si le mot existe et que le mot n'est pas le mot saisi
				console.log('Ok : ' + mot2 + " ajouté");
				let i = dicPhon.indexOf(mot2);
				if(dicMot[i] != mot){
					l.push(dicMot[i]); //On ajoute le mot dans la liste l des mots compatibles
				}
			}
		}

	}
	console.log("liste mot compatible " + l);
	choixMotCompatible(mot, l);

}


//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------

//Fonction qui remplace a un index donné, une lettre donnée.
String.prototype.replaceAt = function(index, replacement) {
	if (index >= this.length) {
		return this.valueOf();
	}

	var chars = this.split('');
	chars[index] = replacement;
	return chars.join('');
}

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
			mot2 = mot2.replaceAt(i,alph[j]); //On remplace la lettre du mot par la lettre de l'alphabet
			console.log(mot2);
			if (motExiste(mot2,dicMot) && mot2 != mot) { //Si le mot existe et que le mot n'est pas le mot saisi
				console.log('Ok : ' + mot2 + " ajouté");
				let i = dicMot.indexOf(mot2);
				if(dicMot[i] != mot){
					l.push(dicMot[i]); //On ajoute le mot dans la liste l des mots compatibles
				}
			}
		}

	}
	console.log("liste mot compatible " + l);
	choixMotCompatible(motSave,l);
}



//Prototype de la fonction principale, en enlevant x lettres du mot rensigné et y lettres du mot recherché
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


	//code de Louis Perret traduit en JS, bug pour l'instant 
	
	let listeCouple = recupCoupleLettre(y, '', [], alph); //Récupère la liste de combinaisons possibles de longueur y
	for (var i = 0; i < mot.length; i++) //Pour chaque lettre de notre mot
	{
		var coupleLettre = recupCouple(mot, x, i); //on recupère le prochain couple de lettre à échanger //lettre[0] dans pyrhon = i ici normalement
	}
		if (coupleLettre[0] == 'true') //S'il existe un couple possible à échanger
	{
		for (couple in listeCouple) //Pour chaque combinaison possible
		{
			let nvtMot = replaceBetween(mot, couple, i, x); //On remplace

			//if coupleLettre[1] != couple and isInDico('word', nvtMot): //Si le mot existe et si on n'a pas remplacer par les mêmes lettres

			let aInsererDansl = [nvtMot, coupleLettre[1], couple];
			l.push(aInsererDansl);
			//l.extend(verificationEspace(nvtMot, (lettre[0], coupleLettre[1]), couple)) < - à revoir
		}
	}
	choixMotCompatible(motSave, l);
	
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
	console.log(x);
	if (x > 1) //Si on désire récupérer un couple de plus de 2 lettres
		if (index + 1 == mot.lenght) //Si on est à la fin du mot(evite les index out of range)
			return ['false', '']; //Exemple: bonjour, si on est à la lettre r, on peut pas prendre de couple avec r car on est à la fin
	return ['true', mot.substring(index, index+x)];
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
	for (l in alphabet)
	{
		if (y == 1)
			listeCouple.push(a + l);
		else
			listeCouple = recupCoupleLettre(y - 1, a + l, listeCouple);
	}
	return listeCouple
}

//Remplace une partie de mot par nvpartie, depuis indexDebut et pendant longueur charactères
function replaceBetween(mot, nvPartie, indexDebut, longueur) {
	console.log(mot.substring(0, indexDebut) + nvPartie + mot.substring(indexDebut, mot.lenght).substring(longueur, mot.lenght));// doit pouvoir être simplifié
};



function updateBtn() {
	let mo = document.getElementById('mot').value;
	mot=mo.toLowerCase(); //On recuperer en minuscule le mot saisi au clavier
	console.log("mot :" + mot);

	var iButton = $(this).val();
	console.log("test click " + iButton);

	aideLettreRechDico(mot,iButton);
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
	//var valeur = document.getElementById("button")


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



//Fonction qui va trouver 2 mots pour former le groupe des 4 mots
function chercheMotDico(lettre1,lettre2,resMot1,resMot2) {
	for(let i=0;i<dicMot.length;i++){ //Pour chaque mots du dico
		let mot1=dicMot[i]; //On prend le premier mot

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


//Fonction qui va trouver la difference de lettre entre deux mots
function aideLettreRechDico(mot1,mot2,resMot1,resMot2) {
	for (let i=0; i<mot1.length; i++) { //Pour chaque lettre du mot 1 (mot saisi)

		if (mot1[i] != mot2[i]) { //Si la lettre au meme indice n'est pas la meme sur les 2 mots
			var lettreMot1 = mot1[i]; //On stock les 2 lettres qui changent
			var lettreMot2 = mot2[i];
			break;
		}

	}
	var resMot1=[]; //on crée 2 tableaux pour accueuillir tous les mots qui vont etre trouvés
	var resMot2=[];
	chercheMotDico(lettreMot1,lettreMot2,resMot1,resMot2);//fonction pour trouver les 4 mots
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





