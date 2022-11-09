from pprint import pprint
import nltk
import json
from pymystem3 import Mystem
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
m = Mystem()
morph = MorphAnalyzer()

class book_analyzer:
    def __init__(self, book):
        self.book = book
        self.book_text, self.analyzed_book = self.mystemize(self.book)
        self.pymd_text = self.do_pymorphy()
        self.lemmd_list = self.lemmatize()
        self.text_cleaning()
        self.data = self.get_parameters()

    def mystemize(self, book):
        with open(book, encoding="utf-8") as f:
            text = f.read()
        analyzed_book = m.analyze(text)
        with open('analized_book.json', 'w', encoding='utf-8') as f:
            json.dump(analyzed_book, f, ensure_ascii=False)

        return text, analyzed_book

    def do_pymorphy(self):
        tokens = word_tokenize(self.book_text)
        pymorphized_text = []
        for token in tokens:
            pym = morph.parse(token)  # morphologically analise text
            pymorphized_text.append(pym)
        return pymorphized_text

    def lemmatize(self):
        lemmatized_list = []
        for item in self.pymd_text:
            unit = item[0]
            lemmatized_list.append([unit.normal_form, unit.tag.POS])

        with open('lemmatized_text_pymorphy.json', 'w', encoding='utf-8') as f:
            json.dump(lemmatized_list, f, ensure_ascii=False)

        return lemmatized_list

    def convert(self, tag):
        if tag is None:
            return tag
        else:
            return str(tag)

    def get_parameters(self):  # a list with words' parameters
        parameters = []

        for item in self.pymd_text:
            unit = item[0]
            parameters.append(({
                'word': self.convert(unit.word),
                'lemma': self.convert(unit.normal_form),
                'POS': self.convert(unit.tag.POS),
                'animacy': self.convert(unit.tag.animacy),
                'aspect': self.convert(unit.tag.aspect),
                'case': self.convert(unit.tag.case),
                'gender': self.convert(unit.tag.gender),
                'involvement': self.convert(unit.tag.involvement),
                'mood': self.convert(unit.tag.mood),
                'number': self.convert(unit.tag.number),
                'person': self.convert(unit.tag.person),
                'tense': self.convert(unit.tag.tense),
                'transitivity': self.convert(unit.tag.transitivity),
                'voice': self.convert(unit.tag.voice)}))

        return parameters

    def text_cleaning(self):
        punct = """!"#$%&\'()*+,./:;<=>?@[\\]^_-`–{|}~«»"""
        for char in punct:
            for i in self.lemmd_list:
                if char == i:
                    self.lemmd_list.remove(char)
        return self.lemmd_list

    def get_topn_pos(self, pos, topn=20):
        pos_list = []
        for unit in self.lemmd_list:
            if unit[1] == pos:
                pos_list.append(unit[0])
        pos_total = Counter(pos_list)
        topn_pos = pos_total.most_common(topn)
        return topn_pos

    def find_ngrams(self, ngram_number=10):
        ngrams = nltk.bigrams(self.lemmd_list)
        grams = []
        for g in ngrams:
            grams.append(g)
        ngramm_total = Counter(grams)
        ngram = ngramm_total.most_common(ngram_number)
        return ngram

    def visualize_pos_proportion(self):
        part = []
        for i in self.lemmd_list:
            part.append(i[1])
        total = Counter(part)
        self.parts = list(total.items())

        dataframe = pd.DataFrame(self.data)

        # scatter plot: X-asis quantity of POS usage; Y-asis POS

        X = []
        Y = []

        for i in range(len(self.parts)):
            X.append(str(self.parts[i][0]))
            Y.append(self.parts[i][1])

        plt.scatter(Y, X, color='MediumAquamarine')
        plt.title('quantities of pos in my book')
        plt.ylabel('parts of speech')
        plt.xlabel('quantity')
        plt.show()

