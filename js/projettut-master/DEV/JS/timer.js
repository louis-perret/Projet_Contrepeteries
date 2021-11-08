var secondes = 0;
var minutes = 1;
var on = false;
var reset = false;

$("#play").click(function(){
    Start();
});
$("#pause").click(function(){
  Stop();
});
$("#reset").click(function(){
  Reset();
});
$("#pen").click(function(){
	Penalite();
})



function chrono(){
  if(minutes>= 1 && secondes==0){
    minutes-=1;
    secondes=59;
  }
  else
    secondes -= 1;
 
if(minutes == 0 && secondes <= 0){
    Stop();
    end=true;
}
 
  affTimer();
}
 
 
function Start(){
  
  if(on===false){
  pts=0;
    timerID = setInterval(chrono, 1000);
    on = true;
    reset = false;
  }   
}
 
  
 
function Stop(){
  if(on===true){
    on = false;
    clearTimeout(timerID);
  }
}



function Penalite(){
  if(minutes == 0 && secondes <= 0){
    Stop();
    end=true;
    

}
if(minutes==0 && secondes < 3){
  secondes=0;
  Stop();
    end=true;
}

  else if(minutes>= 1 && secondes==0){
    minutes-=1;
    secondes=57;
  }
  else
    secondes -= 3;

  affTimer();

}
  


function affTimer(){
  if(minutes<10 && secondes<10){
    $("#timer").html("0"+minutes+" : 0"+secondes);
  }
    else if(minutes<10 && secondes>=10){
      $("#timer").html("0"+minutes+" : "+secondes);
  }
  else if(minutes>=10 && secondes<10){
      $("#timer").html(+minutes+" : 0"+secondes);
  }
  else if(minutes>=10 && secondes>10){
      $("#timer").html(+minutes+" : "+secondes);
  }
}

function Reset(){
  if(reset===false)
  {
    clearInterval(timerID);
    secondes = 0;
    minutes = 1;
    $("#timer").html("01 : 00");
    reset = true;
  }
  on = false;
}