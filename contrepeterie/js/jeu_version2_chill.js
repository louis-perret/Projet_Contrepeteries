var dic=[];
var dicMot=[];
var dicPhon=[];
var dicClassesGram=[];
var dicCle=[];
let dicMot4a8lettres=[];
let alph = "b,d,f,g,k,l,m,n,ŋ,ɲ,p,ʁ,s,ʃ,t,v,z,ʒ,j,w,ɥ,a,ɑ,e,ɛ,ː,ə,i,œ,ø,o,ɔ,u,y,ɑ̃,ɛ̃,œ̃,ɔ̃".split(",");
let score = 0;
let nbSoumissionReponse = 0;
let streak = 0;
let nbMots = 10;

let listeReponse=[];

let motATrouver=[];


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
        dicClassesGram.push(dic[i]['data'][3]);
        if(dic[i]['data'][0].length >= 4 && dic[i]['data'][0].length <= 8 ) {
            let classesGramMot = dicClassesGram[i].replace("['", "").replace("']","").split("', '");
            classesGramMot.forEach(element => {
                if(element !== "verbe")
                    dicMot4a8lettres.push(dic[i]['data'][0]);
            });
        }
    }
    console.log("Affichage du dictionaire de mots");
    console.log(dicMot);
    console.log("Affichage du dictionaire de sons");
    console.log(dicPhon);
    console.log("Affichage du dictionaire des mots de 4 à 8 lettres");
    console.log(dicMot4a8lettres);
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
            console.log("All done!");
            console.log(dic);
            console.log("Appel de split dic");
            splitdic(dic);

        }
    });

    $(function () {
        $.getJSON('../dicoPhoncomFr.json', function (data) {
            console.log(data)
            dicCle = data
        });
    });

    document.querySelector('#myButton').disabled = false;
    document.querySelector('#myButton').addEventListener('mousedown', ()=>{
        document.body.style.cursor = 'wait';
    });
}








function eventListeners() {
    document.querySelector('#myButton').addEventListener('mousedown', event=>{
        document.querySelector('#loadingJeuBeta').style.visibility = "visible";
        document.body.style.cursor = 'wait';
    });

    document.querySelector('#playAgain').addEventListener('mousedown', event=>{
        document.querySelector('#playAgain').style.display = 'none';
        resetAll();
        window.location.href = window.location.href
    });
}

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

function removeButton() {
    var elem = document.getElementById('myButton');
    elem.style.visibility = 'collapse';
    var elemI = document.getElementById('info');
    elemI.style.visibility = 'collapse';
    document.querySelector('div#divLoadingJeuBeta').style.display = 'none';
}

function writeText(motToDisplay){

    var anchor = "<a target='_blank' href='https://fr.wiktionary.org/wiki/"+motToDisplay +"'>" + motToDisplay + "</a>"
    console.log(anchor)

    let lienWiki = "https://fr.wiktionary.org/wiki/" + motToDisplay
    document.getElementById("myH1").innerHTML =anchor
}

function changeStreakPicture(relativePath,w,h) {
    pic = document.querySelector('#streakPicture');
    pic.setAttribute('src',relativePath);
    pic.setAttribute('style',`width: ${w}px; height: ${h}px;`);
}






function returnTuplePhon(x, y, langue, dicVulgaire, valueFiltreGrossier, isClassesGramChecked,mot) {
    let trouveDansDico = false;
    affichResultat = [];
    var l = [];

    if (mot.length == 0)
        return;
    let ind = 0;
    for (let j = 0; j < dicMot.length; j++) { //On trouve l'index de ce mot dans le dico
        if (dicMot[j] == mot) {
            ind = j;
            trouveDansDico = true;
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

    if(trouveDansDico) {
        console.clear
        console.log("indice = "+ind)
        var mot2 = dicPhon[ind]; //On copie ce mot dans mot2
        if (langue == "fr") {
            //lit le fichier ../fr/alphPhonemeFR.txt et rentre le résultat dans la variable globale alph
            jQuery.get("../fr/alphPhonemeFR.txt", function(data) {
                alph = data.split(",");
            });
        }
        else if (langue == "en") {
            jQuery.get("../en/alphPhonemeEN.txt", function(data) {
                alph = data.split(",");
            });
        }

        let motSave = mot2; //On garde le mot en memoire
        let listeCouple = recupCoupleLettre(y, '', [], alph); //Récupère la liste de combinaisons possibles de longueur y
        //console.log("liste couple " + listeCouple)
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

                    nvtMot=nvtMot.replace(" ","");
                    var lengthmot = mot2.length
                    lMot=lengthmot-(x-y);
                    if(motExiste(nvtMot,dicPhon)) {
                        //console.log("Le mot existe !!!!!!!" + nvtMot)
                        var indexMotDic = dicPhon.indexOf(nvtMot)
                        if (mot2 != nvtMot && lMot == nvtMot.length) { //Si le mot existe et si on n'a pas remplacé par les mêmes lettres
                            if(typeof dicClassesGram[dicPhon.indexOf(mot2)] != "undefined" && typeof dicClassesGram[dicPhon.indexOf(nvtMot)] != "undefined") {
                                let isSameClasseGram = false;
                                let substr1 = dicClassesGram[dicPhon.indexOf(mot2)].replace("['", "").replace("']","");
                                let substr2 = dicClassesGram[dicPhon.indexOf(nvtMot)].replace("['", "").replace("']","");
                                let classeGramMot = substr1.split("', '");
                                let classeGramNvtMot = substr2.split("', '");
                                classeGramMot.forEach(element => {
                                    if(classeGramNvtMot.includes(element))
                                        isSameClasseGram = true;
                                });

                                if((isClassesGramChecked && isSameClasseGram) || !isClassesGramChecked) {
                                    if(valueFiltreGrossier == "filtreGrossOnly" && dicVulgaire.includes(dicMot[indexMotDic])) {
                                        l.push(dicPhon[indexMotDic]);
                                    }
                                    else if(valueFiltreGrossier == "filtreGrossNone" && !dicVulgaire.includes(dicMot[indexMotDic])) {
                                        l.push(dicPhon[indexMotDic]);
                                    }
                                    else if(valueFiltreGrossier == "filtreGrossUnabled"){
                                        l.push(dicPhon[indexMotDic]);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        //console.log(" ]")
        //console.log("--------------------------Ma liste compatible : " + l)
        return l;
    }
}



function aideMultiLettreModifViteFait(x, y, monMot) {
    affichResultat = [];
    var l = [];
    let mot = monMot;
    if (mot.length == 0)
        return;
    let ind = 0;
    for (let j = 0; j < dicMot.length; j++) { //On trouve l'index de ce mot dans le dico
        if (dicMot[j] == mot) {
            ind = j;
        }
    }
    var mot2 = dicMot[ind]; //On copie ce mot dans mot2
    var alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
    let motSave = mot2; //On garde le mot en memoire
    let listeCouple = recupCoupleLettre(y, '', [], alph); //Récupère la liste de combinaisons possibles de longueur y
    console.log("Voici donc les lettres que l\'on peut changer :[ ");
    for (var i = 0; i < mot.length; i++) //Pour chaque lettre du mot
    {
        //MOTS COUPES ENLEVES

        var coupleLettre = recupCouple(mot, x, i); //on recupère le prochain couple de lettre à échanger //lettre[0] dans python = i ici normalement
        //console.log("true ou false ? : " + coupleLettre[0])
        if (coupleLettre[0] == 'true') //S'il existe un couple possible à échanger
        {
            console.log(coupleLettre[1] + " , ");
            for (j = 0; j < listeCouple.length; j++) //Pour chaque combinaison possible
            {
                couple = listeCouple[j]
                var nvtMot = mot.replacerAvecIndex(i, x, couple)
                //console.log("NvtMot = " + nvtMot)
                //var nvtMot = replaceBetween(mot, couple, i, x); //On remplace

                nvtMot=nvtMot.replace(" ","");
                //console.log("Mot a tester : " + nvtMot)
                var lengthmot = mot.length
                lMot=lengthmot-(x-y);
                //console.log("longueur mot saisi - diffxy = " + lMot);

                if (nvtMot != mot && motExiste(nvtMot, dicMot) && lMot == nvtMot.length) { //Si le mot existe et si on n'a pas remplacé par les mêmes lettres
                    l.push(nvtMot);
                }
            }
        }
    }
    //document.getElementById("nombreBonnesRep").innerText = "/"+l.length;
    return l;
}




function aideMultiPhonModifViteFait(x, y, langue, monMot) {
    let trouveDansDico = false;
    affichResultat = [];
    var l = [];
    let mot = monMot;
    if (mot.length == 0)
        return;
    let ind = 0;
    for (let j = 0; j < dicMot.length; j++) { //On trouve l'index de ce mot dans le dico
        if (dicMot[j] == mot) {
            ind = j;
            trouveDansDico = true;
            console.log("ind:"+ind)
        }
    }

    if(trouveDansDico) {
        var mot2 = dicPhon[ind]; //On copie ce mot dans mot2

        let motSave = mot2; //On garde le mot en memoire
        console.log(alph)
        let listeCouple = recupCoupleLettre(y, '', [], alph); //Récupère la liste de combinaisons possibles de longueur y
        //console.log(" ########## motSave :  " + motSave.length);
        for (var i = 0; i < motSave.length; i++) //Pour chaque lettre du mot
        {
            //console.log("!!!!! i : " + i)
            var coupleLettre = recupCouple(mot2, x, i); //on recupère le prochain couple de lettre à échanger //lettre[0] dans python = i ici normalement
            //console.log("true ou false ? : " + coupleLettre[0])
            if (coupleLettre[0] == 'true') //S'il existe un couple possible à échanger
            {
                //console.log("hehoçapasselà")
                //console.log(coupleLettre[1] + " , ");
                //console.log(listeCouple.length)
                for (j = 0; j < listeCouple.length; j++) //Pour chaque combinaison possible
                {
                    couple = listeCouple[j]
                    var nvtMot = mot2.replacerAvecIndex(i, x, couple)
                    nvtMot=nvtMot.replace(" ","");
                    console.log("Mot a tester : " + nvtMot)
                    var lengthmot = mot2.length
                    lMot=lengthmot-(x-y);
                    //console.log("longueur mot saisi - diffxy = " + lMot);
                    if(motExiste(nvtMot,dicPhon)) {
                        //console.log("Le mot existe !!!!!!!" + nvtMot)
                        var indexMotDic = dicPhon.indexOf(nvtMot)
                        if (mot2 != nvtMot && lMot == nvtMot.length) { //Si le mot existe et si on n'a pas remplacé par les mêmes lettres
                            l.push(dicMot[indexMotDic]);
                        }
                    }
                }
            }
        }
        return l;
    }
}

function updateScore(streak) {
    score += (10 + streak*10);
    document.querySelector('#displayScore').innerText = score;
}

function resetAll() {
    score = 0;
    streak = 0;
    nbSoumissionReponse = 0;
    listeReponse=[];
    motATrouver=[];
    document.querySelector('h3#solution').innerText = '';
    document.querySelector('h3#messageSuccess').innerText = '';
    document.querySelector('h3#messageFin').innerText = '';
    document.querySelector('h3#displayScore').innerText = '0';
    document.querySelector('h3#streak').innerText = '0';
    changeStreakPicture('../image/ok.png',0,0);
}

function testReponse(motDonne, motEntre) {
    //listeReponse = returnTuplePhon(1, 1, "fr", dicVulgaire, "filtreGrossUnabled", "false",motDonne);
    //pour le moment listeReponse undefined
    /*
    listeReponse.forEach(element => {
        if (element === motEntre)
        console.log("ça marche !!!!")
    });
    */
    listeReponse = aideMultiLettreModifViteFait(1, 1, motDonne);
    listeReponse.forEach(element => {
        if (element === motEntre)
            console.log("ça marche !!!!")
    });

    listeReponsePhon = aideMultiPhonModifViteFait(1, 1, "fr", motDonne);
    listeReponsePhon.forEach(element => {
        if (element === motEntre)
            console.log("!!!! ça marche pour les phonèmes aussi !!!!")
    });
}



function deroulementJeu()
{
    //création liste de mots aléatoire de nbMots mots
    for(let id=0; id<nbMots; id++) {
        let listeReponseNoId = [];
        while(listeReponseNoId.length === 0) {
            posRandom = getRandomInt(dicMot4a8lettres.length);
            console.log(dicMot4a8lettres[posRandom])
            listeReponseNoId = aideMultiLettreModifViteFait(1, 1, dicMot4a8lettres[posRandom])
            listeReponseNoIdPhon = aideMultiPhonModifViteFait(1, 1, "fr", dicMot4a8lettres[posRandom])
            listeReponseNoIdFinale = listeReponseNoId
            listeReponseNoIdPhon.forEach(element => {
                if (!listeReponseNoIdFinale.includes(element)) {
                    listeReponseNoIdFinale.push(element)
                }
            });
        }
        listeReponse.push(listeReponseNoIdFinale);
        motATrouver.push(dicMot4a8lettres[posRandom]);
    }
    removeButton();
    writeText(motATrouver[0])
    startGame();

}

var listeMotReponse=[];

function soumettreReponse()
{

    var nb
    let mot = document.getElementById('reponse').value.toLowerCase();

    if(nbSoumissionReponse === nbMots-1) {
        if (listeReponse[nbSoumissionReponse].includes(mot)) {
            if(!listeMotReponse.includes(mot))
            {
                listeMotReponse.push(mot);
                nb = parseInt(document.getElementById('nombreBonnesRep').innerText);
                nb++
                document.getElementById("nombreBonnesRep").innerText = nb;
                streak++;
                updateScore(streak);
                document.querySelector('h3#messageSuccess').innerText = 'Bonne réponse, tu es un dieu des contrepèteries !';
                document.querySelector('h3#messageSuccess').setAttribute('style', 'color: green;');
            }

        }
        else
        {
            document.getElementById("reponseMot").style.visibility="visible"
            document.querySelector('h3#solution').innerText = '';
            document.querySelector('h3#messageSuccess').innerText = 'Aïe, mauvaise réponse';
            document.querySelector('h3#messageSuccess').setAttribute('style', 'color: red;');
        }

    }

    //let mot = document.getElementById('reponse').value.toLowerCase();
    console.log(mot)
    if (listeReponse[nbSoumissionReponse].includes(mot)) {
        if(!listeMotReponse.includes(mot))
        {
            listeMotReponse.push(mot);
            nb = parseInt(document.getElementById('nombreBonnesRep').innerText);
            nb++
            document.getElementById("nombreBonnesRep").innerText = nb;
            document.getElementById("btnSuiv").style.backgroundColor="#5c8a65"
            document.querySelector('h3#solution').innerText = '';
            document.querySelector('h3#messageSuccess').innerText = 'Bonne réponse, tu es un dieu des contrepèteries !';
            document.querySelector('h3#messageSuccess').setAttribute('style', 'color: green;');
            console.log("gagné")
            streak++;
            updateScore(streak);
        }


    }
    else
    {
        document.getElementById("reponseMot").style.visibility="visible"
        document.querySelector('h3#solution').innerText = '';
        document.querySelector('h3#messageSuccess').innerText = 'Aïe, mauvaise réponse';
        document.querySelector('h3#messageSuccess').setAttribute('style', 'color: red;');
        console.log("perdu")
        streak = 0;
    }
    //nbSoumissionReponse++;

    if(streak >= 3) 
        changeStreakPicture('../image/flamme.png',40,40);
    else if(streak >= 1)
        changeStreakPicture('../image/thumbs_up.png',40,40);
    else
        changeStreakPicture("",0,0)
    document.querySelector('h3#streak').innerText = streak;


}

function waitcursor() {
    document.body.style.cursor = 'wait';
}

function motSuivant()
{
    if(nbSoumissionReponse === nbMots-1) {
        document.querySelector('h3#messageFin').innerText = 'Jeu terminé';
        document.querySelector('h3#messageFin').setAttribute('style','color: #95dabb;');
        let playAgain = document.querySelector('button#playAgain');
        playAgain.style.display = 'inline';
        return;
    }
    listeMotReponse=[]
    //pour prochain mot
    nbSoumissionReponse++;
    writeText(motATrouver[nbSoumissionReponse]);
    document.getElementById("btnSuiv").style.backgroundColor="#343a40"
    document.getElementById('reponse').value = '';
}

function afficherReponse()
{
    const myNode = document.getElementById("solution");
    myNode.innerHTML = '';
    listeReponse[nbSoumissionReponse].forEach(element => {
        let anchor = "<a target='_blank' href='https://fr.wiktionary.org/wiki/"+element +"'>" + element + "</a> ";
        document.querySelector('h3#solution').innerHTML += anchor;
    });

    document.querySelector('h3#messageSuccess').innerText = '';
}

//---------------------------------------
//---------------------------------------
//---------------------------------------

var secondes = 30;
var minutes = 0;
var on = false;
var reset = false;

function startGame(){
    console.log("start game")
    document.querySelector('#loadingJeuBeta').style.display = "none";
    //curseur normal
    document.body.style.cursor = 'default';
    document.getElementById('btnValidate').disabled=false;
    document.getElementById('btnSuiv').disabled=false;
}






function rejouer()
{
    document.querySelector('h3#solution').innerText = '';
    document.querySelector('h3#messageSuccess').innerText = '';
    document.querySelector('h3#messageFin').innerText = 'Perdu ! il faut aller plus vite :)';
    document.querySelector('h3#messageFin').setAttribute('style','color: goldenrod;');
    playAgain = document.querySelector('button#playAgain');
    playAgain.style.display = 'inline';
}
