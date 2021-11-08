import sys

class Arbre:
	
	def __init__(self, m):
		self.mot=m
		self.g=None
		self.d=None
		
		
	def __str__(self):
		return str(self.mot)
	
	def arbrenouv():
		return None	
		
	##Fonction d'insertion	
	def insert(self, m):
		if(self.vide()):
			self=self.e(arbrenouv(),m,arbrenouv())
			return self
		if m == self.r():
			return self
		if m < self.mot:
			if self.g is None:
				self.g = Arbre(m)
			else:
				self.g.insert(m)
		if m > self.mot:
			if self.d is None:
				self.d = Arbre(m)
			else:
				self.d.insert(m)
		self=self.reeq()
		return self			

			
				
	

		

	def r(self):
		return self.mot

				
	def rechercherMot(self, m):
		if self.vide():
			return self
		if m == self.mot:
			return self
		if m < self.mot:
			return rechercherMot(self.g, m);
		if m > self.mot:
			return rechercherMot(self.d, m);
		

	def vide(self):
		return self.mot is None;
	
	def aff(self, level=0):
		if self.d:
			self.d.aff(level+1)
		print(f"{' ' * 4 * level}{self.mot}")
		if self.g:
			self.g.aff(level +1)	

	def haut(self):
		if self == None:
			return 0;
		return 1 + max(self.g.haut() if self.g else 0, self.d.haut() if self.d else 0);
	
	def reeq(self):
		if(self.deseq()==2 and (self.g).deseq()>=0):
			self = self.rd();
		if(self.deseq()==-2 and (self.d).deseq()<=0):
			print("errr")
			self.rg()
			return self	
		if(self.deseq()==2 and (self.g).deseq()==-1):
			self = self.rgd()
		if(self.deseq()==-2 and (self.d).deseq()==1):
			self = self.rdg()
		return self	
	
	def rd(self):
		if (self.vide()):
			return self
		if self.g.vide():
			exit(1) 	
		return self.e((self.g).g, (self.g).r(), self.e((self.g).d,self.r(),self.d))


	def e(self, a, m, b):
		c = Arbre(m)
		c.g=a
		c.d=b
		return c
			
	def rg(self):
		if (self.vide()):
			return self
		if (self.d.vide()):
			exit(1)
		
		return self.e(self.e(self.g,self.r(),self.d.g),self.d.r(),self.d.d)	

	

	def rgd(self):
		if (self.vide()):
			return self
		return self.e(self.g.rg(),self.r(),self.d).rd()
	
	def rdg(self):
		if (self.vide()):
			return self
		return self.e(self.g,self.r(),self.d.rd()).rg()
			
	def deseq(self):
		if(self.vide()):
			return 0;
		if self.g == None and self.d == None:
			return 0	
		if self.g == None:	
			return 0 - self.d.haut()
		if self.d == None:
			return self.g.haut()
		return self.g.haut() - self.d.haut()
					
								
def getDictionnaire():
	a = Arbre("a")
	file = open("testdic.txt", "r")
	lignes = file.readlines()
	for ligne in lignes:
		mot = ligne.rstrip('\n')
		a.insert(mot)
	return a

sys.setrecursionlimit(10000)	
#dic=getDictionnaire();
r=10000
a = Arbre("arbre1")
#a.insert("poney")

#a.insert("pute")

#a.insert("pedale")

#a.insert("putain")

#a.insert("pupupute")
b = Arbre("arbre2")
c =Arbre("thzda")
print("---")
c.insert("z")
c.insert("zz")
c.insert("zzz")
r=c.deseq()
t=c.d.deseq()
print(r)
print(t)
print("---")
c.insert("zzzz")
r=c.deseq()
t=c.d.deseq()
print(r)
print(t)
print("---")
c.insert("zzzzz")
r=c.deseq()
t=c.d.deseq()

print(r)
print(t)
print("---")
c.insert("zzzzzzz")
r=c.deseq()
t=c.d.deseq()
print(r)
print(t)
print("---")
c.aff()

					
#					
#if m < self.mot:
#			if self.g is None:
#				self.g = Arbre(m)
#			else:
#				self.g.insert(m)
#		elif m > self.mot:
#			if self.d is None:
#				self.d = Arbre(m)
#			else:
#				self.d.insert(m)
#		a = self.reeq()
#		print(a)
#		print("----")
#		return a	