import pickle

import numpy as np

from competitor_code.possible_words import possible_words

if __name__ == "__main__":

    data = np.genfromtxt("src/wordle/wiki-100k.txt", dtype="str")

    position = {}  # Lookup table of position in most frequent word list
    for idx, word in enumerate(data):
        word = word.lower()
        if word not in position:
            position[word] = idx

    result = {word: position.get(word, len(possible_words)) for word in possible_words}

    with open("word_use_frequency.pkl", "wb") as f:
        pickle.dump(result, f)

    with open("word_use_frequency.pkl", "rb") as f:
        loaded_dict = pickle.load(f)
