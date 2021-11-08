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


function motExiste(mot, dic){
	if(dic.includes(mot))
		return true;
	return false;
}

function onBtClick(){
	let mot = document.getElementById('mot');	
	suggestionMot(mot.value,dic);
}

function suggestionMot(mot, dic){
	var l=[];
	let mo = document.getElementById('mot').value;
	mot=mot.toLowerCase();
	if(mot in dicMot){
		let ind = dicMot.indexOf(mot);
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
				l.push(dicMot[i]);
			}
		}
	}
	affichageMot(l);
}

function affichageMot(l){
	for(var i=0; i<l.length; i++){
		let par = document.createElement('p');
		par.innerHTML=l[i];
		document.getElementById('div1').append(par);
	}
}


var dic=['cou','rffddo','bru'];
//suggestionMot('cru',dic);
document.getElementById('search').onclick=onBtClick;





