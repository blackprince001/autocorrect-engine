Autocorrect System
==========================================

An autocorrect system predicts that likelihood of a mispelled word to
the correct one.

Steps for Implementing an autocorrect system
----------------------------------------------------------------------------------------------

    1. Identify the mispelled word
    2. Find strings that are `n` edit distance away from the mispelled word
    3. Filter suggested candidates to retain only one found in the vocabulary
    4. Order filtered candidates based on word probabilities
    5. Predict the most likely candidate

Identify a mispelled word
========================================================

A word is mispelled if it is not found in the vocabulary of the corpus
of text the autocorrect system is working with

In [ ]:

    import numpy as np
    import re
    import string
    from collections import Counter
    import json

### Functions for reading texts from files and parsing them into proper data for manipulation.

In [ ]:

    def read_corpus(filename: object) -> list:
        """ Converts filecontents of the filepath(filename)
            into a dictionary list  
        """
        
        with open(filename, 'r') as file:
            lines = file.readlines()
            words = []

            for line in lines:
                words.append(line)

        dictionary = [word.strip('\n\r') for word in words]
        dictionary = [lower.lower() for lower in dictionary]

        return dictionary

    def read_corpus_dataref(filename: object) -> list:
        """ Converts filecontents of the filepath(filename)
            into a dictionary list
        """
        
        with open(filename, 'r') as file:
            lines = file.readlines()
            words = []
            for line in lines:
                words += re.findall(r'\w+', line.lower())

        dictionary = [word.strip('\n\r') for word in words]

        return dictionary

### Reading data from the text file Dictionary.txt and letter.txt into `dictionary` and `data` variables.

In [ ]:

    dictionary = read_corpus('./dictionary.txt')
    data = read_corpus_dataref('./letter.txt')

### Functions to manipulate text from the dictionary list

In [ ]:

    def split_word(word: str) -> list:
        """ Splits words into syllabi """
        return [(word[:i], word[i:]) for i in range(len(word)+1)]

    def insert_word(word: str) -> list:
        """ Inserts words into split words """
        letters = string.ascii_lowercase
        return [l + c + r for l,r in split_word(word) for c in letters]

    def delete_word(word: str) -> list:
        """ Deletes words and letters from split words """
        return [l + r[1:] for l,r in split_word(word) if r]

    def swap_word(word: str) -> list:
        """ Swaps positions of words in split words """
        return [l+r[1]+r[0]+r[2:] for l,r in split_word(word) if len(r) > 1]

    def replace_word(word: str) -> list:
        """ Replaces words and letters in split words """
        letters = string.ascii_lowercase
        return [l+c+r[1:] for l,r in split_word(word) if r for c in letters]

### Implementing levels of Editing to suggest better words from data

In [ ]:

      

    def level_one_edit(word: str) -> list:
        return set(delete_word(word)+swap_word(word)+replace_word(word)+insert_word(word))

    def level_two_edit(word: str) -> list:
        return set(two_edit for two_edits in level_one_edit(word) for two_edit in level_one_edit(two_edits))

    def correct_spelling(word: str, dictionary: list, word_probabilities: float) -> list:
        if word in dictionary:
            return 0

        suggestions = level_one_edit(word) or level_two_edit(word) or [word]
        best_guesses = [w for w in suggestions if w in dictionary]
        
        return sorted([(w, word_probabilities[w]) for w in best_guesses]) 


    vocabs = set(data)
    word_count = Counter(data)
    total_count = float(sum(word_count.values()))
    word_probability = {dict_word: word_count[dict_word]/total_count for dict_word in word_count.keys()}

### Running tests

In [ ]:

    wrong_spelling = 'blakc'
    best = correct_spelling(wrong_spelling, dictionary=vocabs, word_probabilities=word_probability)
    print(f' For the incorrectly spelt word: "{wrong_spelling}", the Most likely word(s) to be correct is/are: "{best}"')

     For the incorrectly spelt word: "blakc", the Most likely word(s) to be correct is/are: "[('black', 0.00033670593516955846), ('blake', 2.0784316985775213e-06), ('blanc', 1.0392158492887607e-06)]"

### Running tests on a text file or stream of text

In [ ]:

    def change(n_tuple: tuple) -> tuple:
        return sorted(n_tuple)[0]

    def parse_text(text: str) -> str:
        lines = text
        words = []

        for line in lines:
            words += re.findall(r'\w+', line.lower())

        parsed_text = [word.strip('\n\r') for word in words]
        return parsed_text

In [ ]:

    sample_text = """Thsi is how it's going to make prediactions"""
    for i in sample_text.lower().split():
        best = correct_spelling(i, vocabs, word_probability)
        if best == 0:
            continue
        print(f'"{i}" can be replaced with "{best}"\n')

    "thsi" can be replaced with "[('phsi', 1.0392158492887607e-06), ('thei', 2.0784316985775213e-06), ('thi', 2.0784316985775213e-06), ('this', 0.003951098658995868)]"

    "it's" can be replaced with "[('its', 0.0011306668440261717), ('itus', 5.196079246443803e-06)]"

    "prediactions" can be replaced with "[('predictions', 2.0784316985775213e-06)]"

YAY!, Everything is working great.[¶](#YAY!,-Everything-is-working-great.) {#YAY!,-Everything-is-working-great.}
--------------------------------------------------------------------------

'thsi' is highly replaceable by 'this' with 0.00039 based on the corpus
used. Greater dataset for the use of this can greatly increase it's
probabilty even it already has the highest amongst the rest of the
predictions made.
