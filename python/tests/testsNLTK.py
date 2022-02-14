import nltk

from nltk.tokenize import word_tokenize
from nltk.tag import StanfordPOSTagger
jar = '../nltk/stanford-postagger-full-2020-11-17/stanford-postagger-4.2.0.jar'
model = '../nltk/stanford-postagger-full-2020-11-17/models/french-ud.tagger'

lotr_quote = "je regarde une jolie personne"

words_in_lotr_quote = word_tokenize(lotr_quote, language="french")
pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' )
lotr_pos_tags = pos_tagger.tag(words_in_lotr_quote)
print(lotr_pos_tags)
grammar = "NP: {<DET>?<NOUN>*<ADJ>}"
chunk_parser = nltk.RegexpParser(grammar)
tree = chunk_parser.parse(lotr_pos_tags)
tree.draw()