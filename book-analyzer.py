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

class BookAnalyzer:
    def __init__(self, book):
        self.book = book
        self.book_text, self.analyzed_book = self.mystemize(self.book)
        self.pymd_text = self.do_pymorphy()
        self.tagged_list = self.tagging()
        self.cleaned_text = self.text_cleaning()
        self.parts = self.get_pos_proportion()
        self.data = self.get_parameters()
        self.bigram_list = self.find_topn_bigrams()

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
            pym = morph.parse(token)
            pymorphized_text.append(pym)
        return pymorphized_text

    def tagging(self):
        tagged_list = []
        for item in self.pymd_text:
            unit = item[0]
            tagged_list.append([unit.normal_form, unit.tag.POS])

        with open('tagged_text.json', 'w', encoding='utf-8') as f:
            json.dump(tagged_list, f, ensure_ascii=False)
        return tagged_list

    def convert(self, tag):
        if tag is None:
            return tag
        else:
            return str(tag)

    def get_parameters(self):
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
        cleaned_text = []
        for i in self.tagged_list:
            cleaned_text.append(i[0])
        punct = """!"#$%&\'()*+,./:;–<=>?@[\\]^_-`{|}~«»"""
        for char in punct:
            for i in cleaned_text:
                if char == i:
                    cleaned_text.remove(char)
        return cleaned_text

    def get_pos_proportion(self):
        part = []
        for i in self.tagged_list:
            part.append(i[1])
        total = Counter(part)
        parts = list(total.items())
        # for i in range(len(parts)):
        #     print(parts[i][0], '-', parts[i][1])
        return parts

    def get_topn_pos(self, pos, topn=20):
        pos_list = []
        for unit in self.tagged_list:
            if unit[1] == pos:
                pos_list.append(unit[0])
        pos_total = Counter(pos_list)
        topn_pos = pos_total.most_common(topn)
        return topn_pos

    def find_topn_bigrams(self, topn=10):
        bigrams = nltk.bigrams(self.cleaned_text)
        grams = []
        bigram_list = []
        for b in bigrams:
            grams.append(b)
        bigramm_total = Counter(grams)
        bigram = bigramm_total.most_common(topn)
        # for i in range(len(bigram)):
        #     print(bigram[i][0], '-', bigram[i][1])
        return bigram_list

    def visualize_pos_proportion(self):
        dataframe = pd.DataFrame(self.data)

        # scatter plot: X-asis number of POS usage; Y-asis POS

        X = []
        Y = []

        for i in range(len(self.parts)):
            X.append(str(self.parts[i][0]))
            Y.append(self.parts[i][1])

        plt.scatter(Y, X, color='MediumAquamarine')
        plt.title('quantities of pos in the text')
        plt.ylabel('parts of speech')
        plt.xlabel('number')
        plt.show()
