import time
import os
import psutil
import matplotlib.pyplot as plt
from statistics import mean
import numpy as np
import math

class Tree:
	def __init__(self, value, left, right):
		self.value = value
		self.left = left
		self.right = right
		self.hauteurG = 0
		self.hauteurD = 0

	def __str__(self):
		return "Tree(%s (%d, %d), %s, %s)" % (self.value, self.hauteurG, self.hauteurD, self.left, self.right)


def insert(tree, value):
	if value < tree.value:
		if tree.left == None:
			tree.left = Tree(value, None, None)
			tree.hauteurG = 1
		else:
			insert(tree.left, value)
			tree.hauteurG = 1 + max(tree.left.hauteurG,
									tree.left.hauteurD)
	else:
		if tree.right == None:
			tree.right = Tree(value, None, None)
			tree.hauteurD = 1
		else:
			insert(tree.right, value)
			tree.hauteurD = 1 + max(tree.right.hauteurG,
									tree.right.hauteurD)

	eq = equilibre(tree)
	if eq > 1:
		if equilibre(tree.left) < 0:
			rotate_left(tree.left)

		rotate_right(tree)

	elif eq < -1:
		if equilibre(tree.right) > 0:
			rotate_right(tree.right)

		rotate_left(tree)

def hauteur(tree):
	if tree == None:
		return 0
	else:
		return max(hauteur(tree.left), hauteur(tree.right)) + 1

def equilibre(tree):
	return tree.hauteurG - tree.hauteurD

def rotate_right(tree):
	tf = tree.left
	(tree.value, tree.left, tree.right,
			tf.value, tf.left, tf.right,
			) = \
	(tf.value, tf.left, tf,
			tree.value, tf.right, tree.right)

	tr = tree.right
	tr.hauteurD = hauteurF(tr.right)
	tr.hauteurG = hauteurF(tr.left)
	
	tree.hauteurD = hauteurF(tree.right)
	tree.hauteurG = hauteurF(tree.left)

	return tree

def hauteurF(t):
	if t == None:
		return 0
	return max(t.hauteurG, t.hauteurD) + 1

def rotate_left(tree):
	tf = tree.right
	(tree.value, tree.right, tree.left,tf.value, tf.right, tf.left,) = \
	(tf.value, tf.right, tf,tree.value, tf.left, tree.left)

	tr = tree.left
	tr.hauteurG = hauteurF(tr.left)
	tr.hauteurD = hauteurF(tr.right)
	
	tree.hauteurG = hauteurF(tree.left)
	tree.hauteurD = hauteurF(tree.right)

	return tree

def rech(tree, value):
	if tree == None:
		return False
	if tree.value == value:
		return True

	if value < tree.value:
		return rech(tree.left, value)

	return rech(tree.right, value)

def empty():
	return Tree(0, None, None)

def getDictionnaire():
	a = Tree("aaa",None, None)
	file = open("dic2.txt", encoding = "ISO-8859-1")
	lignes = file.readlines()

	for ligne in lignes:
		mot = ligne.rstrip('\n')
		insert(a,mot)
	return a

def listeMot():
	l=[]
	file = open("dic2.txt", encoding = "ISO-8859-1")
	lignes = file.readlines()
	for ligne in lignes:
		mot = ligne.rstrip('\n')
		l.append(mot)
	return l	








#chargement arbre
arbre=getDictionnaire()
liste=listeMot()
lMoy=[]

for i in range(1000):
	start_time = time.time()
	#liste de 22740
	for mot in liste:
		boole=rech(arbre, mot)
		#print(boole)

	#for i in range(20000):
	#	boole=rech(arbre,"qererthrzth")	
		#print(boole)

	
	print("Temps d execution : %s secondes " % (time.time() - start_time))
	
	process = psutil.Process(os.getpid())
	print(process.memory_info().rss)
	mem = psutil.virtual_memory()
	print(mem)


	lMoy.append((round((time.time()-start_time),4)))


mi=min(lMoy)
x=[]
while(mi < max(lMoy)):
	x.append(mi)
	mi=mi+0.0001

plt.hist(lMoy,bins = x)
plt.title('Test')
plt.xlabel('Temps d\'exécution en seconde')
plt.ylabel('Nombre d\'occurence')
plt.show()





