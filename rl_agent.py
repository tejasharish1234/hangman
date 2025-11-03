import numpy as np
import random
import string

class RLAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = {}

    def _encode_state(self, masked_word, guessed_letters):
        guessed_count = len(guessed_letters)
        masked_pattern = masked_word.replace("_", "X")  # anonymize blanks
        return (masked_pattern, guessed_count)


    def select_action(self, masked_word, guessed_letters, hmm_probs):
        available = [ch for ch in string.ascii_lowercase if ch not in guessed_letters]
        if np.random.rand() < self.epsilon:
            return random.choice(available)
        state = self._encode_state(masked_word, guessed_letters)
        q_vals = [self.Q.get((state, a), 0) + hmm_probs[ord(a)-97]*5 for a in available]
        return available[np.argmax(q_vals)]

    def update(self, state, action, reward, next_state):
        old_value = self.Q.get((state, action), 0)
        next_max = max([self.Q.get((next_state, a), 0) for a in string.ascii_lowercase], default=0)
        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.Q[(state, action)] = new_value
