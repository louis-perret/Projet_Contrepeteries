var dic=[];
var dicMot=[];
var dicPhon=[];
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


/*var dic=['cou','rffddo','bru'];
//suggestionMot('cru',dic);
document.getElementById('search').onclick=onBtClick;*/





