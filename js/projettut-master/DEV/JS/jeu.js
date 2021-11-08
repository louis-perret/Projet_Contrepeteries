

let t = [
[['Il ','f','ait ','b','eau ',' et ',' ch','aud'],[3,6],['Il fait chaud et beau']],
[['T', 'aisez',' vous',' en',' b','as'],[0,4],['Baisez vous en tas']],
[['Je',' vous',' laisse',' le',' ch','oix',' dans',' la',' d','ate'],[4,8],['Je vous laisse le doigt dans la chatte']],
[['Elle',' revient',' de',' la',' f','erme',' pleine'," d'esp",'oir'],[5,8],['Elle revient de la foire pleine de sperme']]
[['Nul'," n'est",' ja','mais',' assez',' fort',' pour',' ce',' cal','cul'],[3,9],["Nul n'éjacule assez fort pour se calmer"]]
]
//rajouter des contrepèteries


//let sol1 = 'b';
//let sol2 = 'ch';

var selection1=null;
var selection2=null;
var temp=null;

function jouer(index){
	
	let divS = document.getElementById('divSpan');
	if(divS != null){
    	divS.parentNode.removeChild(divS);
	}
    
    let divSpan = document.createElement('div');
    divSpan.id='divSpan';
    document.getElementById('d').append(divSpan);



	for(let i=0; i<t[index][0].length; i++){
		let sp = document.createElement('span');
		sp.setAttribute('class','span');
		sp.innerHTML=t[index][0][i];
		sp.id='span'+i;
		document.getElementById('divSpan').append(sp);	
	}


	for(let j=0;j<t[index][0].length; j++){
		$('#span'+j).click(function(){
			selection(j);
			verif(index);
		});
	}
}


function verif(index){
	if(selection1==document.getElementById('span'+t[index][1][0])&&selection2==document.getElementById('span'+t[index][1][1])||selection2==document.getElementById('span'+t[index][1][0])&&selection1==document.getElementById('span'+t[index][1][1])){
			$('span').unbind("click");
			secondes+=10;
			let soluce= document.createElement('p');
			soluce.innerText=t[index][2];
			soluce.style.color='green';
			document.getElementById('divSpan').append(soluce);
			let bouton= document.createElement('button');
			bouton.innerText="Contrepèterie suivante";
			bouton.id='btnNext';
			document.getElementById('divSpan').append(bouton);
			$('#btnNext').click(function(){
				console.log('erhh');
				jouer(index+1);
				selection1=null;
				selection2=null;
			});

	}

}

function selection(j){
		temp=document.getElementById('span'+j);
		if(temp!=null){
			if(selection1==null|| selection1==''){
				selection1=temp;
				selection1.style.color='blue';
				temp=null;
			}
			else
				if(selection2==null && selection1!=temp || selection2=='' && selection1!=temp){
					selection2=temp;
					selection2.style.color='blue';
					temp=null;
				}
		}
		if(selection1==temp && selection1!=null){
			selection1.style.color='black';
			selection1=null;
		}
		else
			if(selection2==temp && selection2!=null){
				selection2.style.color='black';
				selection2=null;
			}
}


jouer(0)
	