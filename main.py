from __future__ import division
import nltk
import json
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

#Ladda in textfil med innehall att sammanfatta samt fil med ordklasstatistik
f = open("att_tagga.txt", "r")
f1 = open("sucordklassertxt_ordklasstatistik.txt", "r")
stemmer = SnowballStemmer('swedish')
dicts = json.load(f1)
# Dela upp i meningar och lagg i en array
sentences = nltk.sent_tokenize(f.read().decode('utf8'))

# For varje mening ska det ordklasstaggas, stemmas och goras en frekvenslista
tagged_text = []
for sentence in sentences:
    words = nltk.word_tokenize(sentence)
    for word in words:
        if dicts.has_key(word.encode('utf8')):
            tag = sorted(dicts[word.encode('utf8')].items(), key=lambda x:x[1], reverse=True)[0][0]
            tagged_text.append(word + ' ' + tag)
        else:
            tagged_text.append(word + ' ' + 'NN')

# Create frequence list
freq_list = dict()
for word in tagged_text:
    tokens = nltk.word_tokenize(word)
    if tokens[0] not in stopwords.words('swedish') and tokens[1] != 'MAD' and tokens[1] != 'MID' :
        if freq_list.has_key(stemmer.stem(tokens[0])):
            freq_list[stemmer.stem(tokens[0])] += 1
        else:
            freq_list[stemmer.stem(tokens[0])] = 1

    

# Dela alla varden i frekvenslistan med hogsta antalet frekvens for att fa varde mellan 0-1
highest_value = sorted(freq_list.items(),  key=lambda x:x[1], reverse=True)[0][1]
for word in freq_list:
    freq_list[word] = freq_list[word] / highest_value
    
# Kor alla meningar mot frekvenslistan (orden stemmade) och tilldela meningarna en score
ordered = []
for sentence in sentences:
    score = 0
    tokens = nltk.word_tokenize(sentence)
    for token in tokens:
        if freq_list.has_key(stemmer.stem(token)):
            score += freq_list[stemmer.stem(token)]

    ordered.append({
        'sentence': sentence,
        'score': score/len(tokens)
    })


# Plocka ut x antal meningar och gor till sammanfattning
sammanfattning = ""
avg = 0
for s in ordered:
   avg += s['score']
avg = (avg/len(ordered)) * 1.10

for s in ordered:
    if s['score'] > avg:
        sammanfattning += s['sentence'].encode('utf8') + " "
print sammanfattning