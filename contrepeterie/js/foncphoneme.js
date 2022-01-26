var alph = []

//Fonction principale
//Fonction qui rend une liste de mot compatible -> pour code = comme, cognent, cochent,...
//Va ensuite appeler les fonctions pour trouver les groupes de 4 mots
//Traduction de la fonction de généralisation python en JS
function aideMultiPhon(x, y, langue, dicVulgaire, filtreGrossierActivated) {
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

	//récupère le nom de la vue actuelle
	let pathActuel = window.location.pathname;
	let fichierActuel = pathActuel.split("/").pop();
	if(fichierActuel == "aide_a_la_contrepeterie.html") {
		pathToDictionary = "../dict_fr_ok.csv";
		langue = "fr";
	}
	else if (fichierActuel == "spoonerism_aid.html") {
		pathToDictionary = "../debut_dico_en.csv";
		langue = "en";
	}

	if(ind == 0) {
		if(langue == "fr")
			document.getElementById('div1').innerHTML = "Pas de résultat";
		else if(langue == "en")
			document.getElementById('div1').innerHTML = "No result";
		document.getElementById('loadingStats').style.visibility = "collapse";
	}
	else {
		var mot2 = dicPhon[ind]; //On copie ce mot dans mot2
		if (langue == "fr") {
			//lit le fichier ../fr/alphPhonemeFR.txt et rentre le résultat dans la variable globale alph
			jQuery.get("../fr/alphPhonemeFR.txt", function(data) {
				alph = data.split(",");
			});
		}	
		else if (langue == "en") {
			jQuery.get("../fr/alphPhonemeEN.txt", function(data) {
				alph = data.split(",");
			});
		}

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
					console.log("mot2 = " + mot2)

					console.log("i = " + i)
					console.log("x = " + x)
					console.log("couple = " + couple)
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
							if(filtreGrossierActivated) {
								if(!dicVulgaire.includes(dicMot[indexMotDic])) {
									console.log("++++++++++++++++++++++++++++++++++++Mot ajouté : " + nvtMot)
									l.push(dicPhon[indexMotDic]);
								}
							}
							else {
								console.log("++++++++++++++++++++++++++++++++++++Mot ajouté : " + nvtMot)
								l.push(dicPhon[indexMotDic]);
							}
						}	
					
					}
	
				}
			}
		}
		console.log(" ]")
		//console.log("--------------------------Ma liste compatible : " + l)
		choixMotCompatible(motSave, l);
	}
  }

//Fonction qui va trouver la difference de lettres entre deux mots, essentiel pour permettre de trouver le groupe de 4 mots
function aidePhonemRechDico(mot1, mot2) {
	console.log("mot1 !!!!!!!!!!!!!!!!!!!!!!!!!! " + mot1)
	console.log("mot2 !!!!!!!!!!!!!!!!!!!!!!!!!! " + mot2)
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
	chercheMotDicoPhon(lettreMot1,lettreMot2,saveX,saveY,resMot1,resMot2);//fonction pour trouver les 4 mots
	document.getElementById("loadingStats").style.visibility="collapse";
	//On prepare l'affichage des 4 mots un à un
	for (let j = 0; j <resMot1.length ; j++) { //Pour chaque mot de resMot1
		if(mot1 != resMot1[j]) {
			var indexMotDic1 = dicPhon.indexOf(mot1)
			var indexMotDic2 = dicPhon.indexOf(mot2)
			var indexRes1 = dicPhon.indexOf(resMot2[j])
			var indexRes2 = dicPhon.indexOf(resMot1[j])
			affichResultat.push("<div style ='margin: 10px;'><div class='card p-2 shadow-sm'>"+ dicMot[indexMotDic1] + ' - ' + dicMot[indexRes2] + '</div>' + '<div class="card p-2 shadow-sm">' + dicMot[indexMotDic2] + ' - ' + dicMot[indexRes1] +'</div></div>')
		}
	}
	affichageMot(affichResultat);
}

function chercheMotDicoPhon(lettre1,lettre2,x,y,resMot1,resMot2) {
	var diffXY = x - y;
	var longueurMax= document.getElementById("choixLongueurMax").value
	var longueurMin= document.getElementById("choixLongueurMin").value
	for(let i=0;i<dicPhon.length-1;i++){ //Pour chaque mots du dico
		let mot1=dicPhon[i]; //On prend le ieme mot du dico
		lg1=mot1.length;
		longueur1=lg1-diffXY; //Variable pour determiner les longueurs des mots à trouver quand le nombre de lettre à remplacer change
		longueur1plus=lg1+diffXY;
		let posLettre1=mot1.indexOf(lettre1); //On regarde ou la lettre1 est dans ce mot

		if(posLettre1 != -1 && mot1.length<= longueurMax && mot1.length >= longueurMin) { //Si la lettre1 est presente dans le mot 1 du dico + respecte les conditions de longueur
			for(let j=0;j<dicPhon.length-1;j++){ //Pour chaque mot du dico
				let mot2=dicPhon[j]; //On prend le premier mot
				lg2=mot2.length;
				longueur2moins=lg2-diffXY;//Variable pour determiner les longueurs des mots à trouver quand le nombre de lettre à remplacer change
				longueur2plus=lg2+diffXY;

				if (diffXY ==0 ) { //Si on remplace i par i lettres
					//Rentre ici : testé
					if (mot1.length == mot2.length && mot1 != mot2) { //Si les 2 mots sont de meme longueur et ne sont pas les memes
						var lettreCommune = 0;
						for (let k=0;k<mot1.length;k++) { //Pour chaque lettre du mot1 on compte les lettres communes avec le mot 2

							if (mot1[k] == mot2[k]){ //Si la lettre au meme index entre les 2 mots est identique :
								lettreCommune++; //On incremente cette variable
							}
						}
						var posLettre2=mot2.indexOf(lettre2);//On regarde ou la lettre1 est dans ce mot
						if(posLettre2 != -1) { //Si la lettre2 est presente dans le mot 2 du dico
							if (posLettre1 == posLettre2 && lettreCommune == mot1.length-1 && !motExiste(mot1,resMot1) ) { //On regarde si les deux mots ont la lettre1 et la lettre2 au meme endroit
								resMot1.push(mot1); //Et on regarde si le mot2 a toutes ses autres lettres differentes du mot grace a "LettreCommune"
								resMot2.push(mot2);//Si c'est le cas on ajoute les 2 mots dans les tableaux respectifs
								console.log("trouve");
								break;
							}
						}
					}
				}
				if (diffXY > 0 ) { //Si on remplace i+x par i lettres
					//Rentre ici : testé
					if (longueur1 == mot2.length) { //Si le premier mot fait x lettres et le deuxieme fait x lettres de moins
						var lettreCommune = 0;
						var posLettre2=mot2.indexOf(lettre2);//On regarde ou la lettre1 est dans ce mot
						if(posLettre2 != -1 && posLettre1 == posLettre2) {
							mot1test=mot1.replace(lettre1,"") //On garde uniquement les lettres qui ne sont pas a echanger entre les 2 mots
							mot2test=mot2.replace(lettre2,"")
							for (let k=0;k<mot1test.length;k++) { //Pour chaque lettre du mot1 sans ses lettres à echanger

								if (mot1test[k] == mot2test[k]){ //Si la lettre au meme index entre les 2 mots est identique :
									lettreCommune++; //On incremente cette variable
								}
							}
								if (lettreCommune == mot1test.length && !motExiste(mot1,resMot1)) { //On regarde le mot1 et le mot2 ont toutes leurs lettres en commun à part les lettres à echanger
									resMot1.push(mot1);
									resMot2.push(mot2);//Si c'est le cas on ajoute les 2 mots dans les tableaux respectifs
									break;
								}
						}
					}
				}
				if (diffXY < 0 ) {//Si on remplace i par i+y lettres
					if (mot1.length == longueur2plus) { //Si le premier mot fait x lettres et le deuxieme fait y lettres de plus
						var lettreCommune = 0;
						var posLettre2=mot2.indexOf(lettre2);//Meme principe que juste au dessus
						if(posLettre2 != -1 && posLettre1 == posLettre2) {
							mot1test=mot1.replace(lettre1,"")
							mot2test=mot2.replace(lettre2,"")
							for (let k=0;k<mot1test.length;k++) {

								if (mot1test[k] == mot2test[k]){
									lettreCommune++;
								}
							}
							if (lettreCommune == mot1test.length && !motExiste(mot1,resMot1)) {
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
	}
	console.log("Mot 1 : " + resMot1);
	console.log("mot 2 : " + resMot2);
}
