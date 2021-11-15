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

/*function onBtClick(){
	let mot = document.getElementById('mot');	
	suggestionMot();
}*/
/*
function suggestionMot(){
	var l=[];
	let mo = document.getElementById('mot').value;
	mot=mo.toLowerCase();
	console.log("mot :" + mot);
	//console.log(dicMot);
	let ind = 0; 
	console.log(mot + dicMot[3]);
	for(let j=0;j<dicMot.length;j++){
		if(dicMot[j] == mot){
			ind = j;
		}
	}
	mot2=dicPhon[ind];
	//var alph=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];

	var alph = ['b', 'd', 'f', 'g', 'k', 'l', 'm', 'n', 'ŋ','ɲ','p','ʁ','s', 'ʃ', 't', 'v', 'z', 'ʒ', 'j', 'w','ɥ', 'a', 'ɑ', 'e', 'ɛ','ɛː','ə','i', 'œ','ø','o','ɔ','u','y','ɑ̃','ɛ̃','œ̃','ɔ̃'];
	var m=mot2.split('');
	console.log(m);
	
	for(var i=0; i<m.length; i++){
		console.log(m[i]);
		for(var j=0;j<alph.length;j++){
			var mcopy=m.slice(0);
			mcopy[i]=alph[j];
			//console.log(mcopy);
			var mcopyjoin=mcopy.join('');
			console.log(mcopyjoin);
			if(motExiste(mcopyjoin,dicPhon) && mcopyjoin != mot){
				console.log('Ok');
				let i = dicPhon.indexOf(mcopyjoin);
				if(dicMot[i] != mot){
					l.push(dicMot[i]);
				}
				
			}
		}
	}
	affichageMot(l);
}
*/

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
//Fonction principale
//Fonction qui rend une liste de mot compatible -> pour code = gode, cote, iode...
//Va ensuite appeler les fonctions pour trouver les groupes de 4 mots
function aideLettreSubs() {
	affichResultat=[];
	var l=[];
	let mo = document.getElementById('mot').value;
	mot=mo.toLowerCase(); //On recuperer en minuscule le mot saisi au clavier
	console.log("mot :" + mot);
	//console.log(dicMot);
	let ind = 0;
	for(let j=0;j<dicMot.length;j++){ //On trouve l'index de ce mot dans le dico
		if(dicMot[j] == mot){
			ind = j;
		}
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





