#!/bin/bash

longueurMot=$1
longueurCouple=$2
log=$3
cpu=$(lscpu | grep GHz | cut -d " " -f 33 | sed -re 's/GHz//g' | sed -re 's/\.[0-9]{2}//g')
cpu=$(($cpu*100000))
complex=$((26**$longueurCouple))
complex=$(($complex*$longueurMot*$log))
tpsExec=$(($complex/$cpu))
echo "Temps d'exécution : $tpsExec secondes"