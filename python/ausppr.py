from arbin import *
import json
import itertools
import sys

sys.stdout.reconfigure(encoding='utf-8')

phrase = "salut a toi jeune homme"
phrase = phrase.split()
Lphrases = [[phrase]] #phrase se contient elle même
word = phrase[0]

k = []
k.append([ranger,manger,0,1])
print(k)