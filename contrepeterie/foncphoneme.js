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

//Fonction qui va trouver la difference de lettres entre deux mots, essentiel pour permettre de trouver le groupe de 4 mots
function aidePhonemRechDico(mot1, mot2) {

	console.log("phonem!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	document.getElementById('loadingStats').style.visibility = "collapse";
	document.getElementById("bRetour").setAttribute("class","mt-3");
	affichResultat=[]
	x=document.getElementById("choixDeX").value;
	y=document.getElementById("choixDeY").value;
	var lettreMot1 = "";
	var lettreMot2 = "";
	let saveX = x;
	let saveY = y;

	//code	 de			d					code		de			d
	//comme  mmme		mmm					cogne		gn			gn

	var passage = 0;
	for (var i=0; i<mot1.length; i++) { //Pour chaque lettre du mot 1 (mot saisi)

		if (mot1[i] != mot2[i]) { //Si la lettre au meme indice n'est pas la meme sur les 2 mots
			console.log("Lettre differentes : " + mot1[i] + " " + mot2[i])

			if(i+1==mot1.length){
				var lettreApres = mot1[i];
			} else {
				lettreMot1 = lettreMot1 + mot1[i];
				var lettreApres = mot1[i+1]
			}
			console.log("Lettre suivante du mot 1 : " + lettreApres)
			for (let j=i+passage; j<mot2.length;j++) {
				console.log("lettre du mot 2 a tester : " + mot2[j])
				if(mot2[j] == lettreApres) {
					passage=passage+1
					console.log("La lettre egale est " + mot2[j])
					break;
				} else {
					console.log("La lettre a push est " + mot2[j])
					lettreMot2 = lettreMot2 + mot2[j];
				}
			}
		}

	}

	//console.log("lettre numero " + i)
	//console.log("lettre a tester 1 " + mot1[i])
	//console.log("lettre a tester 2 " + mot2[i])
	//lettreMot1 = lettreMot1 + mot1[i];
	//lettreMot2 = lettreMot2 + mot2[i];

	console.log("lettres1 " + lettreMot1)
	console.log("lettres2 " + lettreMot2)
	var resMot1=[]; //on crée 2 tableaux pour accueuillir tous les mots qui vont etre trouvés
	var resMot2=[];
	chercheMotDico(lettreMot1,lettreMot2,saveX,saveY,resMot1,resMot2);//fonction pour trouver les 4 mots
	document.getElementById("loadingStats").style.visibility="collapse";
	//On prepare l'affichage des 4 mots un à un
	for (let j = 0; j <resMot1.length ; j++) { //Pour chaque mot de resMot1
		if(mot1 != resMot1[j]) {
			affichResultat.push('<div class="card p-2 shadow-sm" style="width: 18rem;">'+ mot1 + ' - ' + resMot2[j] + '</div>'  ); //On ajoute dans une variable globale
			affichResultat.push('<div class="card p-2 shadow-sm" style="width: 18rem;">' + mot2 + ' - ' + resMot1[j] +'</div>');//Le mot saisi - le mot avec la lettre du mot2
			affichResultat.push('<hr width="50">');        //Le mot 2 (compatible) - le mot avec la lettre du mot1
		}
	}
	affichageMot(affichResultat);
}