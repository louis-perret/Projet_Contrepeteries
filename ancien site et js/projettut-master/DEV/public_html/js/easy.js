
//[[''],[,],[""]],
var tabContrepeterie = [
[['F','i','ght','ing ','a ',' l','i','ar'],[0,5],['Lighting a fire']],
[['You ', 'h','i','ss','ed ','my ','m','yst','ery ','l','ect','ure'],[1,6],['You missed my history lecture']],
[['B','a','tt','le ','sh','ips ','and ','c','rui','sers'],[0,7],['Cattle ships and bruisers']],
[['N','os','ey ','l','i','tt','le ','c','ook'],[0,7],['Cosy little nook']],
[['A ','bl','u','sh','ing ','cr','ow'],[1,5],["A crushing blow"]],
[['T','ons ','of ','s','oil'],[0,3],["Sons of toil"]],
[['Our ','quee','r ','old ','Dea','n'],[1,4],["Our dear old Queen"]],
[['We ','w','ill ','ha','ve ','the ','h','ags ','fl','ung ','out'],[6,8],["We will have the flags hung out"]],
[['G','o ','and ','t','a','ke ','a ','sh','o','wer'],[3,7],["Go and shake a tower"]],
[['L','a','ck ','of ','p','i','es'],[0,4],["Pack of lies"]],
[['B','a','t ','fl','a','tt','ery'],[0,3],["Flat battery"]],
[['I ','hit ','my ','b','u','nn','y ','ph','o','ne'],[3,7],["I hit my funny bone"]],
[['Fl','u','tt','er ','b','y'],[0,4],["Butterfly"]],
[["F",'i','ve ','of ','Cl','ubs'],[0,4],["Clive of Fubbs"]],
[['L','ead ','of ','sp','i','te'],[0,3],["Speed of light"]],
[['Fl','i','pp','ing ','the ',' ch','a','nn','el ','on ','TV'],[0,5],["Chipping the flannel on TV"]]
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
			secondes+=20;
			let soluce= document.createElement('p');
			soluce.innerText=tabContrepeterie[index][2];
			soluce.style.color='green';
			soluce.setAttribute('id','soluce');
			document.getElementById('divSpan').append(soluce);
			let bouton= document.createElement('button');
			bouton.innerText="Next spoonerism";
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
	