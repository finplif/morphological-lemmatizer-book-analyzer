# Morphological Book Analyzer

## This class allows to:
* **mystemize(book)** – get morphological analysis for each word in text
* **do_pymorphy()** – get morphological analysis for each word in text with all the wordforms considered (makes sense for russian language)
* **tagging()** – return a .json file with lemmas for each word and their part of speech
* **get_parameters()** – return a list with parameters for each word in text (word, lemma, POS, animacy, aspect, case, gender, involvement, mood, number, person, tense, transitivity, voice)
* **text_cleaning()** – return a list with lemmas of the text words without punctuation
* **get_pos_proportion()** – return a list with each part of speech and the number of usage in text
* **get_topn_pos(pos, topn=20)** – return a list with top 20 words of a particular part of speech
* **find_topn_bigrams(topn=10)** – return a list with top 10 bigramms in text
* **visualize_pos_proportion()** – shows a plot with parts of speech and their number of usage in text

## Files description:
* **crime-and-punishment.txt** – original text
* **analized_book.json** – original text with a morphological analysis for each word 
* **tagged_text.json** – a file with lemma and part of speech for each word in the original text
