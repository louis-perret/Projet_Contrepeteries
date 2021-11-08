
//[[''],[,],[""]],
var tabContrepeterie = [
[['Att','en','tion',' v','ous',' vi','dez',' vos',' n','ouilles',' sur',' ma',' c','ape'],[8,12],["Attention vous videz vos couilles sur ma nappe"]],
[['A','voir',' une',' gro','sse',' b','oî','te',' plei','ne',' de',' p','i','les'],[6,12],["Avoir une grosse bite pleine de poils"]],
[['Co','mment',' par','ler',' de',' P','a','pe',' au',' Conc','i','le'],[6,10],["Comment parler de pipes aux cons sales"]],
[['Elle',' re','vient',' de',' la',' f','erme',' pl','eine'," d'esp",'oir'],[6,10],['Elle revient de la foire pleine de sperme']],
[['Elle',' ha','bite',' La','val'],[2,4],["Elle avale la bite"]],
[['Nul'," n'est",' ja','mais',' assez',' fort',' pour',' ce',' cal','cul'],[3,9],["Nul n'éjacule assez fort pour se calmer"]],
[['A','llons',' ma',' fi','lle,',' e','ssuie',' ça',' v','ite',' et',' b','ien'],[8,11],["Allons ma fille, essuie sa bite et viens"]],
[['Elle',' ai','me',' le',' t','enn','is',' en',' p','en','sion'],[4,8],["Elle aime le pénis en tension"]],
[['Ce',' va','cc','in,',' quel',' su','j','et'],[2,6],["Ce vagin, quel succès"]],
[['Att','en','tion',' le',' p','ont',' va',' c','ass','er'],[4,7],["Attention le con va passer"]],
[['Se',' com','pri','mer',' la',' p','anse',' quand',' on',' d','îne'],[6,10],["Se comprimer la pine quand on danse"]],
[['Chr','oni','queur',' de',' gr','oupes'],[0,4],["Gros niqueur de croupes"]],
[['F','ête',' de',' la',' b','ière'],[1,5],["Fière de la bête"]],
[['T', 'ai','sez',' v','ous',' en',' b','as'],[0,6],['Baisez vous en tas']],
[['Ce','tte',' gran','de',' p','êch','euse',' de',' L','ine'],[4,8],["Cette grande lécheuse de pine"]],
[["C’est",' l','ong',' co','mme',' la','c','une'],[1,6],["C’est con comme la lune"]],
[['C','ai','sse',' de',' f','arine'],[0,4],["Fesses de Karine"]],
[['Il',' f','ait ',' b','eau',' et',' ch','aud'],[3,6],['Il fait chaud et beau']],
[['Bou','ch','ée',' à',' la',' r','eine'],[1,5],["Bourrée à la chaîne"]],
[['Dé','bit','er',' les',' compt','es'],[1,4],["Décompter les bites"]],
[['Des',' n','ou','illes,',' en','c','ore'],[1,5],["Des couilles en or"]],
[['Une',' c','u','vette',' pl','eine',' de',' b','ou','illon'],[1,7],["Une buvette pleine de couillons"]],
[['Je',' v','ous',' lai','sse',' le',' ch','oix',' dans',' la',' d','ate'],[6,10],['Je vous laisse le doigt dans la chatte']],
[['Elles',' ont',' tou','tes',' un',' t','oit',' pour',' se',' d','ou','cher'],[5,9],["Elles ont toutes un doigt pour se toucher"]]
]
//rajouter des contrepèteries


//let sol1 = 'b';
//let sol2 = 'ch';

var selection1=null;
var selection2=null;
var temp=null;
var indexj=0;

function jouer(index){
	
	let divS = document.getElementById('divSpan');
	if(divS != null){
    	divS.parentNode.removeChild(divS);
	}
    
    let divSpan = document.createElement('div');
    divSpan.id='divSpan';
    document.getElementById('d').append(divSpan);



	for(let i=0; i<tabContrepeterie[index][0].length; i++){
		let sp = document.createElement('span');
		sp.setAttribute('class','span');
		sp.innerHTML=tabContrepeterie[index][0][i];
		sp.id='span'+i;
		document.getElementById('divSpan').append(sp);	
	}


	for(let j=0;j<tabContrepeterie[index][0].length; j++){
		$('#span'+j).click(function(){
			selection(j);
			verif(index);
		});
	}
}


function verif(index){
	if(selection1==document.getElementById('span'+tabContrepeterie[index][1][0])&&selection2==document.getElementById('span'+tabContrepeterie[index][1][1])||selection2==document.getElementById('span'+tabContrepeterie[index][1][0])&&selection1==document.getElementById('span'+tabContrepeterie[index][1][1])){
			$('span').unbind("click");
			indexj++;
			secondes+=5;
			let soluce= document.createElement('p');
			soluce.innerText=tabContrepeterie[index][2];
			soluce.style.color='green';
			soluce.setAttribute('id','soluce');
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
	