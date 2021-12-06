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
	for (let j = 0; j < dicMot.length; j++) { //On trouve l'index de ce mot dans le dico
		if (dicMot[j] == mot) {
			ind = j;
		}
	}
	var mot2 = dicPhon[ind]; //On copie ce mot dans mot2
	var alph = ['b', 'd', 'f', 'g', 'k', 'l', 'm', 'n', 'ŋ','ɲ','p','ʁ','s', 'ʃ', 't', 'v', 'z', 'ʒ', 'j', 'w','ɥ', 'a', 'ɑ', 'e', 'ɛ','ɛː','ə','i', 'œ','ø','o','ɔ','u','y','ɑ̃','ɛ̃','œ̃','ɔ̃'];
	let motSave = mot2; //On garde le mot en memoire
	let listeCouple = recupCoupleLettre(y, '', [], alph); //Récupère la liste de combinaisons possibles de longueur y
	console.log(" ########## motSave :  " + motSave.length);
	for (var i = 0; i < motSave.length; i++) //Pour chaque lettre du mot
	{
		//console.log("!!!!! i : " + i)
		var coupleLettre = recupCouple(mot2, x, i); //on recupère le prochain couple de lettre à échanger //lettre[0] dans python = i ici normalement
		//console.log("true ou false ? : " + coupleLettre[0])
		if (coupleLettre[0] == 'true') //S'il existe un couple possible à échanger
		{
			console.log(coupleLettre[1] + " , ");
			for (j = 0; j < listeCouple.length; j++) //Pour chaque combinaison possible
			{
				couple = listeCouple[j]
				var nvtMot = mot2.replacerAvecIndex(i, x, couple)
				console.log("NvMot = " + nvtMot)
				//var nvtMot = replaceBetween(mot, couple, i, x); //On remplace
  
				nvtMot=nvtMot.replace(" ","");
				console.log("Mot a tester : " + nvtMot)	
				var lengthmot = mot2.length
				lMot=lengthmot-(x-y);
				console.log("longueur mot saisi - diffxy = " + lMot);
				if(motExiste(nvtMot,dicPhon)) {
					console.log("Le mot existe !!!!!!!" + nvtMot)
					var indexMotDic = dicPhon.indexOf(nvtMot)
					if (mot2 != nvtMot && lMot == nvtMot.length) { //Si le mot existe et si on n'a pas remplacé par les mêmes lettres
						console.log("++++++++++++++++++++++++++++++++++++Mot ajouté : " + nvtMot)
						l.push(dicMot[indexMotDic]);
					}	
				
				}
  
			}
		}
	}
	console.log(" ]")
	//console.log("--------------------------Ma liste compatible : " + l)
	choixMotCompatible(mot, l);
	
  }
