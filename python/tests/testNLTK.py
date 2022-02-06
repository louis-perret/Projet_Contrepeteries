import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#ltk.download('tagsets')

from nltk.tokenize import word_tokenize,sent_tokenize


"""
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
"""
sentence="j'ai une belle frite et vous "
sentence=word_tokenize(sentence,language="french")
#entence=nltk.pos_tag(sentence)
#nltk.help.upenn_tagset()
#print(sentence)

from nltk.tag import StanfordPOSTagger
jar = '../nltk/stanford-postagger-full-2020-11-17/stanford-postagger-4.2.0.jar'
model = '../nltk/stanford-postagger-full-2020-11-17/models/french-ud.tagger'

pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' )
res = pos_tagger.tag(sentence)
print (res)