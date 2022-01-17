import math

def calculTempsExecution(longueurMot,longueurCoupleLettre):
	complexite=pow(26,longueurCoupleLettre)
	complexite=complexite*longueurMot*math.log(320000,10)
	tempsExecution=complexite/2000000000
	#if tempsExecution <= 1:
	#	tempsExecution = "Moins de 0 secondes"
	print(f"Temps d'exécution : {tempsExecution}")

