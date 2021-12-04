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


//NE MARCHE PAS

//Fonction principale
//Fonction qui rend une liste de mot compatible -> pour code = comme, cognent, cochent,...
//Va ensuite appeler les fonctions pour trouver les groupes de 4 mots
//Traduction de la fonction de généralisation python en JS
function aideMultiPhon(x, y) {

	//replaceBetween(document.getElementById('mot').value, "ch", x, 2);
	affichResultat = [];
	var l = [];
	let mot = document.getElementById('mot').value.toLowerCase(); //On recuperer en minuscule le mot saisi au clavier
	if (mot.length == 0)
		return;
	let ind = 0;
	for (let j = 0; j < dicPhon.length; j++) { //On trouve l'index de ce mot dans le dico
		if (dicPhon[j] == mot) {
			ind = j;
		}
	}
	var mot2 = dicPhon[ind]; //On copie ce mot dans mot2
	var alph = ['b', 'd', 'f', 'g', 'k', 'l', 'm', 'n', 'ŋ','ɲ','p','ʁ','s', 'ʃ', 't', 'v', 'z', 'ʒ', 'j', 'w','ɥ', 'a', 'ɑ', 'e', 'ɛ','ɛː','ə','i', 'œ','ø','o','ɔ','u','y','ɑ̃','ɛ̃','œ̃','ɔ̃'];
	let motSave = mot2; //On garde le mot en memoire
	let listeCouple = recupCoupleLettre(y, '', [], alph); //Récupère la liste de combinaisons possibles de longueur y
	console.log("Voici donc les lettres que l\'on peut changer :[ ");
	for (var i = 0; i < mot.length; i++) //Pour chaque lettre du mot
	{
  
		//pour les mots coupés, mais ne marche pas -> seulement une lettre et un espace est échangée (pas 2 lettres et un espace par exemple, dans le cas x=2 y=1)
		for (let j = 0; j < alph.length; j++) { //Pour chaque lettre de l'alphabet {
			mot2 = mot2.replaceAt(i, alph[j]); //On remplace la lettre du mot par la lettre de l'alphabet
			var tabVerifEspaces = verificationEspaces(mot, mot[i], mot2[i], i);
			mot2temp=mot2.replace(" ","");
			var lengthmot = mot.length
			lMot=lengthmot-(x-y);
  
			if (tabVerifEspaces != "" && lMot == mot2temp.length)
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
  
				nvtMot=nvtMot.replace(" ","");
				console.log("Mot a tester : " + nvtMot)	
				var lengthmot = mot.length
				lMot=lengthmot-(x-y);
				console.log("longueur mot saisi - diffxy = " + lMot);
				
				var i = dicPhon.indexOf(nvtMot);
				if (dicMot[i] != nvtMot && motExiste(nvtMot, dicPhon) && lMot == nvtMot.length) { //Si le mot existe et si on n'a pas remplacé par les mêmes lettres
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
  