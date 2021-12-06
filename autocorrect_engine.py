import numpy as np
import re
import string
from collections import Counter
import json


def read_corpus(filename: object) -> list:
    """Converts filecontents of the filepath(filename)
    into a dictionary list
    """

    with open(filename, "r") as file:
        lines = file.readlines()
        words = []

        for line in lines:
            words.append(line)

    dictionary = [word.strip("\n\r") for word in words]
    dictionary = [lower.lower() for lower in dictionary]

    return dictionary


def read_corpus_dataref(filename: object) -> list:
    """Converts filecontents of the filepath(filename)
    into a dictionary list
    """

    with open(filename, "r") as file:
        lines = file.readlines()
        words = []

        for line in lines:
            words += re.findall(r"\w+", line.lower())

    dictionary = [word.strip("\n\r") for word in words]

    return dictionary


dictionary = read_corpus("./autocorrect-engine/dictionary.txt")
data = read_corpus_dataref("./autocorrect-engine/letter.txt")


def split_word(word: str) -> list:
    """Splits words into syllabi"""
    
    return [(word[:i], word[i:]) for i in range(len(word) + 1)]


def insert_word(word: str) -> list:
    """Inserts words into split words"""
    
    letters = string.ascii_lowercase
    
    return [l + c + r for l, r in split_word(word) for c in letters]


def delete_word(word: str) -> list:
    """Deletes words and letters from split words"""
    
    return [l + r[1:] for l, r in split_word(word) if r]


def swap_word(word: str) -> list:
    """Swaps positions of words in split words"""
    
    return [l + r[1] + r[0] + r[2:] for l, r in split_word(word) if len(r) > 1]


def replace_word(word: str) -> list:
    """Replaces words and letters in split words"""
    
    letters = string.ascii_lowercase
    
    return [l + c + r[1:] for l, r in split_word(word) if r for c in letters]


def level_one_edit(word: str) -> list:
    
    return set(
        delete_word(word) + swap_word(word) + replace_word(word) + insert_word(word)
    )


def level_two_edit(word: str) -> list:
    
    return set(
        two_edit
        for two_edits in level_one_edit(word)
        for two_edit in level_one_edit(two_edits)
    )


def correct_spelling(word: str, dictionary: list, word_probabilities: float) -> list:
    
    if word in dictionary:
        return 0

    suggestions = level_one_edit(word) or level_two_edit(word) or [word]
    best_guesses = [w for w in suggestions if w in dictionary]

    return sorted([(w, word_probabilities[w]) for w in best_guesses])


vocabs = set(data)
word_count = Counter(data)

total_count = float(sum(word_count.values()))

word_probability = {
    dict_word: word_count[dict_word] / total_count for dict_word in word_count.keys()
}


wrong_spelling = "blakc"

best = correct_spelling(
    wrong_spelling, dictionary=vocabs, word_probabilities=word_probability
)

print(
    f' For the incorrectly spelt word: "{wrong_spelling}", the Most likely word(s) to be correct is/are: "{best}"'
)


def change(n_tuple: tuple) -> tuple:

    return sorted(n_tuple)[0]


def parse_text(text: str) -> str:
    lines = text
    words = []

    for line in lines:
        words += re.findall(r"\w+", line.lower())

    parsed_text = [word.strip("\n\r") for word in words]

    return parsed_text


sample_text = """Thsi is how it's going to make prediactions"""

for i in sample_text.lower().split():
    best = correct_spelling(i, vocabs, word_probability)

    if best == 0:
        continue

    print(f'"{i}" can be replaced with "{best}"\n')
