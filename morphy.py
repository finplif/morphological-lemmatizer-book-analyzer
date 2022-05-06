from pprint import pprint
import json
from pymystem3 import Mystem
import nltk
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
from nltk.corpus import stopwords
import seaborn as sns

m = Mystem()

with open("spotted-band.txt", encoding="utf-8") as f:
    text = f.read()

analyzed_text = m.analyze(text)

with open('spotted-band.json', 'w', encoding='utf-8') as f:
    json.dump(analyzed_text, f, ensure_ascii=False)

tokens = word_tokenize(text)


morph = MorphAnalyzer()


def convert(tag):
    if tag is None:
        return tag
    else:
        return str(tag)
        

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



        
data = []

for item in pymd_text:
    unit = item[0]
    data.append(({'word': convert(unit.word), 'lemma': convert(unit.normal_form),
'POS': convert(unit.tag.POS), 'animacy': convert(unit.tag.animacy),
'aspect': convert(unit.tag.aspect), 'case': convert(unit.tag.case),
'gender': convert(unit.tag.gender), 'involvement': convert(unit.tag.involvement),
'mood': convert(unit.tag.mood), 'number': convert(unit.tag.number),
'person': convert(unit.tag.person), 'tense': convert(unit.tag.tense),
'transitivity': convert(unit.tag.transitivity), 'voice': convert(unit.tag.voice)}))


df = pd.DataFrame(data)
print(df.head(5))



lemmd_list = []
for item in pymd_text:
    unit = item[0]
    lemmd_list.append([unit.normal_form, unit.tag.POS])
    
    
part = []
for i in lemmd_list:
    part.append(i[1])
total = Counter(part)
parts = list(total.items())



X = []
Y = []

for i in range(len(parts)):
    X.append(str(parts[i][0]))
    Y.append(parts[i][1])

plt.scatter(Y, X, color='MediumAquamarine')
plt.title('quantities of pos in my book')
plt.ylabel('parts of speech')
plt.xlabel('quantity')
plt.show()



verb = []
for unit in lemmd_list:
    if unit[1] == 'VERB':
        verb.append(unit[0])
verb_total = Counter(verb)
verbs = verb_total.most_common(5)



X = []
Y = []

for i in range(len(verbs)):
    X.append(verbs[i][0])
    Y.append(verbs[i][1])
    
plt.bar(X, Y, color='LightPink')
plt.title('5 глаголов и их количество в книге')
plt.ylabel('количество употреблений')
plt.xlabel('глаголы')
plt.show()



adverb = []
for unit in lemmd_list:
    if unit[1] == 'ADVB':
        adverb.append(unit[0])
adverb_total = Counter(adverb)
adverbs = adverb_total.most_common(420)



text = ' '.join([adverbs[i][0] for i in range(len(adverbs))])

wordcloud = WordCloud(
    background_color ='white',
    width = 1200,
    height = 1200,
).generate(text)

plt.figure(figsize = (10, 10), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.title('облако наречий')
plt.show()



plt.figure(figsize=(7, 7))
df['case'].value_counts().plot(kind='pie')
plt.title('cases')
plt.show()




df2 = df[['animacy', 'case', 'gender']].groupby(['animacy', 'case'], as_index=False).count()
df2.columns = ['animacy', 'case', 'total']
df2 = df2[df2['total'] > 10]

plt.figure(figsize=(10, 6))
sns.boxplot(x = "case", y = "total", data = df2)
plt.ylim((0, 2200))
plt.title('N of animas entries by case')
plt.ylabel('n entries')
plt.xlabel('case');
plt.show()
