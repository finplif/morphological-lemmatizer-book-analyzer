# Morphological Book Analyzer

?? description

## This class allows to:
* **mystemize(book)** – get morphological analysis for each word in text
* **do_pymorphy()** – get morphological analysis for each word in text with all the wordforms considered (makes sense for russian language)
* **tagging()** – return a .json file with lemmas for each word and their part of speech
* **get_parameters()** – return a list with parameters for each word in text (word, lemma, POS, animacy, aspect, case, gender, involvement, mood, number, person, tense, transitivity, voice)
* **text_cleaning()** – return a list with lemmas of the text words without punctuation
* **get_pos_proportion()** – 
* **get_topn_pos(self, pos, topn=20)** – 
* **find_ngrams(self, ngram_number=10)** – 
* **visualize_pos_proportion(self)** – 

## Files description:
* **** – original text
* **** – original text lemmatized and cleaned from punctuation with each sentence on a new line
* **** – all the words listed from the new-text.txt
