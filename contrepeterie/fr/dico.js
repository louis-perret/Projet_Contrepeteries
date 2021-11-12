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

function load2(){
	splitdic(dic);
}

function processData(allText) {
    var record_num = 2;  // or however many elements there are in each row
    var allTextLines = allText.split(/\r\n|\n/);
    var entries = allTextLines[0].split(',');
    var lines = [];

    var headings = entries.splice(0,record_num);
    while (entries.length>0) {
        var tarr = [];
        for (var j=0; j<record_num; j++) {
            tarr.push(headings[j]+":"+entries.shift());
        }
        lines.push(tarr);
    }
    console.log(line);
}



function charge(data) {

	arr = data.split(/\r?\n/);

	var dic = {};
	for(let index in arr){
		var line = arr[index];
		line = line.split(',');
		var word = line[0];
		console.log(line);
		if(line[0] == '')
			continue;
		var pron = line[1].split(' ');
		dic[word]=pron;
	}
	genererContrepeterie("Elle a le choix dans la date".split(" "), dic);
}

function generer(){

}



function genererContrepeterie(){
	console.log(dic);
	//pour chaque mot de la phrase
	let phrase = document.getElementById('phrase').value;
	console.log(phrase);
	phrase=phrase.trim();
	let phrA = phrase.split(' ');
	let index = [];
	for(let i=0; i<phrA.length; i++){
		if(dicMot.includes(phrA[i])){
			index.push(dicMot.indexOf(phrA[i]))
		}
		else{
			console.log('mot existe pas' + phrA[i]);
		}
	}
	console.log(index);
	let pronList = [];
	let son2;

	index.forEach( ind => {
		
		let son=dicPhon[ind].split(' ');
		son.forEach(s => pronList.push(s.split('')));
		});
	console.log("pronlist " + pronList);
	
	for(let wI=0; wI<pronList.length; wI++){
		console.log('Wi' + wI);
		for(let sI=1; sI<pronList[wI].length; sI++){
			console.log('si '+ sI);
			for(let sif=0; sif<(pronList[wI].length-sI+1); sif++){
				console.log("sif " + sif);
				for(let rwi=wI+1; rwi<pronList.length; rwi++){
					console.log("rwi " + rwi);



					if(sI <= pronList[rwi].length){
						console.log("si < pronlist[rwi].length OKOK");


						for(let sis=0; sis<pronList[rwi].length-sI+1; sis++){
							console.log("sis " + sis);
							let pronListTest= pronList.slice();
							console.log("PronListTest " + pronListTest);
							for(let index1=sis; index1<sis+sI; index1++){
								for(let index2=sif; index2<sif+sI;index2++){
									if(pronListTest[rwi][index1] == pronListTest[wI][index2]){
										continue;
									}

									
									 for (let i = 0; i < sI; i++) {
                                        tmp = pronListTest[wI][index1+i];
                                        pronListTest[wI][index1+i] = pronListTest[rwi][index2+i];
                                        pronListTest[rwi][index2+i] = tmp;
                                    }
									


									if (pronListTest[wI] in dicPhon && pronListTest[rwi] in dicPhon) {
										console.log("debug 5");
										console.log(pronListTest[wI]);
										let keys1 = getRes(pronListTest[wI]);
										let keys2 = getRes(pronListTest[wI]);
										console.log("son " + keys1, keys2);
										let p = phrase.slice();
										console.log("phrase " + p);
										p = p.split(' ');
										console.log("phrase " + p);
										p[wI] = keys1;
										p[rwi] = keys2;
										p = p.join();
										console.log("normal " + p);
									}
									/*if(pronListTest[rwi].values()){
										if (wI > 0) {
											
										}
									}*/


								}
						}
					}
				}
			}
		}
	}	
}}

function getRes(pw1){
	if(pw1 in dicPhon){
		let ind=dicPhon.indexOf(pw1);
		console.log("ind " + ind);
		console.log(dicMot[ind]);
		return dicMot[ind];
	}
}


