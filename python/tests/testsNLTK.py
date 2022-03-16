import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('tagsets')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
#nltk.download('conll2000')

from nltk.tokenize import word_tokenize
from nltk.tag import StanfordPOSTagger
jar = '../nltk/stanford-postagger-full-2020-11-17/stanford-postagger-4.2.0.jar'
model = '../nltk/stanford-postagger-full-2020-11-17/models/french-ud.tagger'

#Tests
tabPhrases=[]
tabPhrases.append("je regarde une jolie personne") #marche
tabPhrases.append("je une jolie personne") #marche pas
tabPhrases.append("je regarde une personne") #marche
tabPhrases.append("la personne regarde") #marche
tabPhrases.append("je regarde personne") #marche pas
tabPhrases.append("regarde une jolie personne") #marche pas
tabPhrases.append("une regarde jolie personne") #marche pas -> il dit que ça marche alors qu'elle est fausse -> faudra faire des règles plus précises

pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' )
"""
for i in range(len(tabPhrases)): #pour chaque phrase on tokenize, puis on tag
    tabPhrases[i] = word_tokenize(tabPhrases[i], language="french")
    tabPhrases[i] = pos_tagger.tag(tabPhrases[i])
"""

#test avec des patterns simples
def testChunking(tabPhrases):
    grammar = """
                NP: {<DET>?<NOUN><ADJ>}
                NP: {<DET>?<ADJ>*<NOUN>}
                CP: {<PRON|DET|NP><VERB><NP>?}
                """ #définis un chunck


    chunk_parser = nltk.RegexpParser(grammar)
    for i in range(len(tabPhrases)):
        phrase = word_tokenize(tabPhrases[i], language="french")
        phrase = pos_tagger.tag(phrase)
        tree=chunk_parser.parse(phrase)
        b=False
        tabElements=tree.productions()[0].rhs() #on récupère la partie droite du premier résultat du parsage 
        #print(tabElements)
        for element in tabElements: #on parcours les éléments
            if(isinstance(element,nltk.grammar.Nonterminal)): #si c'est un élément non terminal et non un tuple
                if(element.symbol() == "CP"): #s'il contient l'élément qu'on a voulu vérifier
                    b=True

        if(b): #si true -> phrase juste
            print(f"Phrase : {tabPhrases[i]} -> juste")
        else:
            print(f"Phrase : {tabPhrases[i]} -> pas juste")

    return tree

#Marche pas
def accuracy(phrase):
    from nltk.corpus import conll2000
    grammar = r"NP: {<DET>?<ADJ>*<NOUN>}"
    cp = nltk.RegexpParser(grammar)
    phrase=conll2000.chunked_sents(phrase, chunk_types=['NP'])
    print(cp.evaluate(phrase))


testChunking(tabPhrases)
#accuracy(phrase)


