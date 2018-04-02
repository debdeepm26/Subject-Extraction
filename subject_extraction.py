import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')

NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']

def clean_document(document):
    document = re.sub('[^A-Za-z .-]+', ' ', document)
    document = ' '.join(document.split())
    document = ' '.join([i for i in document.split() if i not in stop])
    return document

def tokenize_sentences(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    return sentences

def get_entities(document):
    entities = []
    sentences = tokenize_sentences(document)

    sentences = [nltk.pos_tag(sent) for sent in sentences]
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                entities.append(' '.join([c[0] for c in chunk]).lower())
    return entities

def word_freq_dist(document):
    words = nltk.tokenize.word_tokenize(document)
    words = [word.lower() for word in words if word not in stop]
    fdist = nltk.FreqDist(words)
    return fdist

def extract_subject(document):
    fdist = word_freq_dist(document)
    most_freq_nouns = [w for w, c in fdist.most_common(10)
                       if nltk.pos_tag([w])[0][1] in NOUNS]

    entities = get_entities(document)
    top_10_entities = [w for w, c in nltk.FreqDist(entities).most_common(10)]

    subject_nouns = [entity for entity in top_10_entities
                    if entity.split()[0] in most_freq_nouns]
    return subject_nouns

if __name__ == '__main__':
    doc = open('GWBUsh.txt', 'r')
    docname = doc.name
    document = open('GWBUsh.txt', 'r').read()
    document = clean_document(document)
    subject = extract_subject(document)
    print('dataDocument.txt is created')
    j=len(subject)-1
    file = open("dataDocument.txt","w")
    file.write('"')
    file.write(str(docname))
    file.write('",[')
    while(j>=0):
        file.write('"')
        file.write(str(subject[j]))
        file.write('"')
        if j>=1:
            file.write(',')
        j=j-1
    file.write(']')
    file.close()
