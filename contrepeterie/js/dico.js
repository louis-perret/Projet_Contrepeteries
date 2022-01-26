var dic=[];
var dicMot=[];
var dicPhon=[];


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

}

$(document).ready(function(){
	$("#csv-file").change(handleFileSelect);
});

function splitdicSelector(){
	for(let i=0; i<dic[0]['data'].length; i++){
		dicMot.push(dic[0]['data'][i][0]);
		dicPhon.push(dic[0]['data'][i][1]);
	}
	console.log("Affichage du dictionaire de mots");
	console.log(dicMot);
	console.log("Affichage du dictionaire de sons");
	console.log(dicPhon);
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



function loadDico(){
	document.getElementById('chargement').innerHTML = '<div class="loading"></div>';


	let pathToDictionary = "../dict_fr_ok.csv";

	Papa.parse(pathToDictionary, {
		download: true,
		step: function(row) {
			dic.push(row);
		},
		complete: function() {
			document.getElementById('chargement').innerHTML = '<div id="wrapper"><svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none" /><path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8" /></svg></div>';
			document.getElementById('chargement').style.backgroundColor="beige";
			//document.getElementById('loadDico').disabled=true;
			console.log("All done!");
			console.log(dic);
			console.log("Appel de split dic");
			splitdic(dic);

		}
	});
}



function mainRecherchePhrase() {
	var phrase=document.getElementById('phrase').value;
	mainMixSyllabes(phrase,"lettre");
}

//Debut de la fonction pour trouver resultat dans phrases //

function mainMixSyllabes(phrase,mode) {
	var phrase = phrase.split(' ')
	var Lphrases = []
	var tmp = []
	var taille
	var test

	Lphrases.push() //ohrase contient elle meme
	//console.log(Lphrases)
	//console.log(phrase)

	//Pour chaque mot dans la phrase
	for (var i in phrase) {
		//console.log(i)
		var j=parseInt(i) + 1;

		for (var j;j<phrase.length;j++) {
			var WordsContreP = mixSyllableWord(phrase[i], phrase[j], phrase,mode)
			//console.log("WordContreP :")
			//console.log(WordsContreP)
			for (k in WordsContreP) {
				//console.log("k = " + k)
				tmp = [].concat(phrase)
				/*
				console.log("tmp i = " + tmp[i])
				console.log("WordsContreP[k] = " + WordsContreP[k][0])
				console.log("tmp j = " + tmp[j])
				console.log("WordsContreP[k] = " + WordsContreP[k][1])
				*/
				tmp[i] = WordsContreP[k][0]
				tmp[j] = WordsContreP[k][1]
				taille = phrase.length
				test = true
				for(let l=0;l<taille;l++) {
					if(phrase == tmp) {
						test = false
					}
					if(test) {
						var L1 = ([parseInt(i),WordsContreP[k][2][0],WordsContreP[k][2][1]])
						var L2 = ([j,WordsContreP[k][3][0],WordsContreP[k][3][1]])
						console.log(tmp)
						console.log(L1)
						console.log(L2)
						console.log("lphrase :")	
						console.log(Lphrases)
						if(!Lphrases.includes("<div style='margin: 10px;'><div class='card p-2 shadow-sm'>"+ phrase.join(' ') + '</div>' + '<div class="card p-2 shadow-sm">' + tmp.join(' ') +'</div></div>')) {
							Lphrases.push("<div style='margin: 10px;'><div class='card p-2 shadow-sm'>"+phrase.join(' ') + '</div>' + '<div class="card p-2 shadow-sm">' + tmp.join(' ') +'</div></div>')
						}
						
					}
				}
				
			}
		}
	}
	affichageMot(Lphrases)
		
	
}



function mixSyllableWord(word1,word2,phrase,mode) {
	listeWord = [];
	tmp = Array();
	var i = 0;
	var j = 1;
	while(i<word1.length) {
		//console.log(word1)
		//console.log(word1.length)
		//console.log(i)

		tmp = mixSyllableWord2(word1.slice(i,j),word2,phrase,mode)
		console.log("----------------------------------------- " )
		//console.log(tmp)

		for (k in tmp) { //Pour cette partie j'ai fais j-1 mais coté python c'est juste j mais j'ai l'impression que ca ne marche pas si je fais pas j-1
			//console.log("tmp : " + tmp)
			//console.log("mot de tmp  : " + word1.slice(0,i) + tmp[k][1] + word1.slice(j))
			if (motExiste(word1.slice(0,i)+tmp[k][1]+word1.slice(j),dicMot)) {
				listeWord.push([word1.slice(0,i)+tmp[k][1]+word1.slice(j), tmp[k][0],[i,j],tmp[k][2]])
				//console.log("le mot " + word1.slice(0,i) + " " + tmp[k][1] + " " + word1.slice(j-1) + " a été ajouté")
				/*
				console.log(k + "----------------------")
				console.log("word 1 ? : " + word1) 
				console.log("i : " + i)
				console.log(word1.slice(0,i))
				console.log(tmp[k][1])
				console.log(word1.slice(j))
				console.log(tmp[k][0])
				console.log([i,j])
				console.log(tmp[k][2])*/
			}
		}
		j+=1
		if (j>word1.length) {
			i+=1
			j=i+1
		}
		return listeWord
	}
}

function mixSyllableWord2(sy,word2,phrase,mode) {
	i = 0;
	j = 1;
	liste = [];
	while(i<word2.length) {

		mot = word2.slice(0,i) + sy + word2.slice(j)
		if (motExiste(mot,dicMot)) {
			liste.push([mot,word2.slice(i,j),[i,j]])
		}
		j+=1;
		if (j>word2.length) {
			i+=1
			j=i+1
		}
		return liste

	}
}

	function motExiste(mot, dic){
		if(dic.includes(mot))
			return true;
		return false;
	}




