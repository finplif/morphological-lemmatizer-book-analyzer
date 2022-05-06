from pprint import pprint
import json
from pymystem3 import Mystem
import nltk
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer
from collections import Counter

m = Mystem()

with open("spotted-band.txt", encoding="utf-8") as f:
    text = f.read()

analyzed_text = m.analyze(text)

with open('spotted-band.json', 'w', encoding='utf-8') as f:
    json.dump(analyzed_text, f, ensure_ascii=False)

tokens = word_tokenize(text)


morph = MorphAnalyzer()



pymd_text = []

for token in tokens:
    pym = morph.parse(token)
    pymd_text.append(pym)


lemmd_list = []
for item in pymd_text:
    unit = item[0]
    lemmd_list.append([unit.normal_form, unit.tag.POS])
    
    
with open('spotted-band_pymorphy.json', 'w', encoding='utf-8') as f:
    json.dump(lemmd_list, f, ensure_ascii=False)


part = []
for i in lemmd_list:
    part.append(i[1])
total = Counter(part)
parts = list(total.items())
"""
for i in range(len(parts)):
    print(parts[i][0], '-', parts[i][1])
"""


summa = len(text)
"""
for i in range(len(parts)):
    print(parts[i][0], 'составляет ', parts[i][1]/summa, 'долю')
"""


verb = []
for unit in lemmd_list:
    if unit[1] == 'VERB':
        verb.append(unit[0])
verb_total = Counter(verb)
verbs = verb_total.most_common(20)
for i in range(len(verbs)):
    print(verbs[i][0], '-', verbs[i][1])
    
    
adverb = []
for unit in lemmd_list:
    if unit[1] == 'ADVB':
        adverb.append(unit[0])
adverb_total = Counter(adverb)
adverbs = adverb_total.most_common(20)
for i in range(len(adverbs)):
    print(adverbs[i][0], '-', adverbs[i][1])
    
    
    
lemmas = []
for i in lemmd_list:
    lemmas.append(i[0])
    
punct = """!"#$%&\'()*+,./:;<=>?@[\\]^_-`{|}~«»–"""
for char in punct:
    for i in lemmas:
        if char == i:
            lemmas.remove(char)


bigrams = nltk.bigrams(lemmas)
bis = []
for b in bigrams:
    bis.append(b)
bi_total = Counter(bis)
bi = bi_total.most_common(25)
for i in range(len(bi)):
    print(bi[i][0], '-', bi[i][1])
    
    
trigrams = nltk.trigrams(lemmas)
tris = []
for t in trigrams:
    tris.append(t)
tri_total = Counter(tris)
tri = tri_total.most_common(25)
for i in range(len(tri)):
    print(tri[i][0], '-', tri[i][1])
