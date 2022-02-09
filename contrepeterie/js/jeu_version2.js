var dic=[];
var dicMot=[];
var dicPhon=[];
var dicCle=[];


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

    $(function () {
        $.getJSON('../dicoPhoncomFr.json', function (data) {
            console.log(data)
            dicCle = data
        });
    });
}