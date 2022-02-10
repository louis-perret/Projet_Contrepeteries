import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('tagsets')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
from nltk.tokenize import word_tokenize,sent_tokenize


"""
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
"""
sentence="j'ai de belles frites et vous "
sentence=word_tokenize(sentence,language="french")
#entence=nltk.pos_tag(sentence)
#nltk.help.upenn_tagset()
#print(sentence)

from nltk.tag import StanfordPOSTagger
jar = '../nltk/stanford-postagger-full-2020-11-17/stanford-postagger-4.2.0.jar'
model = '../nltk/stanford-postagger-full-2020-11-17/models/french-ud.tagger'

pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' )
res = pos_tagger.tag(sentence)
#print (res)

from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import FrenchStemmer
wnl = WordNetLemmatizer()

def isplural(word):
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural, lemma

"""
nounls = ['geese', 'mice', 'bars', 'foos', 'foo', 
              'families', 'family', 'dog', 'dogs']
              """
nounls = ['chiens', "mères", 'maires', 'homme', 'doigt', 
              'orteils', "maison", 'maisons', 'aventuriers']
"""
for nn in nounls:
    isp, lemma = isplural(nn)
    print(nn, lemma, isp)
"""
"""
import treetaggerwrapper
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')
tags = tagger.tag_text("pip install treetaggerwrapper")
print(tags)
"""
#---------------------------------------