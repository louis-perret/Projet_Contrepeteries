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
String.prototype.replaceAt = function(index, replacement) {
	if (index >= this.length) {
		return this.valueOf();
	}

	var chars = this.split('');
	chars[index] = replacement;
	return chars.join('');
}

function aideLettreSubs() {
	affichResultat=[];
	var l=[];
	let mo = document.getElementById('mot').value;
	mot=mo.toLowerCase();
	console.log("mot :" + mot);
	//console.log(dicMot);
	let ind = 0;
	for(let j=0;j<dicMot.length;j++){
		if(dicMot[j] == mot){
			ind = j;
		}
	}
	var mot2=dicMot[ind];
	var alph=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
	let motSave=mot2; //On garde le mot en memoire

	for (let i=0; i<mot2.length; i++) {
		mot2=motSave;
		for(let j=0;j<alph.length;j++) {
			mot2 = mot2.replaceAt(i,alph[j]);
			console.log(mot2);
			if (motExiste(mot2,dicMot) && mot2 != mot) {
				console.log('Ok : ' + mot2 + " ajouté");
				let i = dicMot.indexOf(mot2);
				if(dicMot[i] != mot){
					l.push(dicMot[i]);
				}
			}
		}

	}
	for (let k = 0; k <l.length ; k++) {
		aideLettreRechDico(motSave,l[k]);
	}


}

function chercheMotDico(lettre1,lettre2,resMot1,resMot2) {
	for(let i=0;i<dicMot.length;i++){
		let mot1=dicMot[i];

		let posLettre1=mot1.indexOf(lettre1);

		if(posLettre1 != -1 && mot1.length<5) { //Si la lettre1 est presente dans le mot 1 du dico
			for(let j=0;j<dicMot.length;j++){
				let mot2=dicMot[j];
				if (mot1.length == mot2.length && mot1 != mot2 ) {
					var lettreCommune = 0;
					for (let k=0;k<mot1.length;k++) {

						if (mot1[k] == mot2[k]){
							lettreCommune++;
						}
					}
					var posLettre2=mot2.indexOf(lettre2);
					if(posLettre2 != -1) { //Si la lettre2 est presente dans le mot 2 du dico
						if (posLettre1 == posLettre2 && lettreCommune == mot1.length-1 ) {
							resMot1.push(mot1);
							resMot2.push(mot2);
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

function aideLettreRechDico(mot1,mot2,resMot1,resMot2) {
	for (let i=0; i<mot1.length; i++) {

		if (mot1[i] != mot2[i]) {
			var lettreMot1 = mot1[i];
			var lettreMot2 = mot2[i];
			break;
		}

	}
	var resMot1=[];
	var resMot2=[];
	chercheMotDico(lettreMot1,lettreMot2,resMot1,resMot2);
	for (let j = 0; j <resMot1.length ; j++) {
		affichResultat.push('<b>' + mot1 + '</b>&#9;' + ' - ' + resMot2[j] );
		affichResultat.push(mot2 + ' - ' + resMot1[j] );
		affichResultat.push('----------------');
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





