import numpy as np
import string

class HMM:
    def __init__(self, corpus_path="Data/corpus.txt"):
        self.letter_probs = self._train(corpus_path)

    def _train(self, corpus_path):
        letters = {ch: 1 for ch in string.ascii_lowercase}  # start with smoothing
        with open(corpus_path, "r") as f:
            for line in f:
                for ch in line.strip().lower():
                    if ch in letters:
                        letters[ch] += 1
        total = sum(letters.values())
        return {ch: letters[ch] / total for ch in letters}

    def get_letter_probs(self, masked_word, guessed_letters):
        probs = np.array([self.letter_probs[ch] for ch in string.ascii_lowercase])
        for g in guessed_letters:
            if g in string.ascii_lowercase:
                probs[ord(g) - 97] = 0
        probs = probs / np.sum(probs)
        return probs
