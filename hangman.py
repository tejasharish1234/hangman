import os
import random

class hangman:
    # Vars
    played_word = ""
    gameboard = []
    gameboard_finished = []
    guess = ''
    guess_archive = []
    lives = []
    end_state = False
    word_list = []

    def __init__(self):
        # Load only 5 words from the corpus.txt file
        try:
            with open("Data/corpus.txt", "r") as f:
                for i, line in enumerate(f):
                    self.word_list.append(line.strip())
                    if i == 4:  # Stop after 5 words
                        break
        except FileNotFoundError:
            print("Error: corpus.txt not found in Data folder.")
            self.word_list = ['default', 'backup', 'words', 'for', 'hangman']

    def set_Word(self):
        word = random.choice(self.word_list)
        self.played_word = word

    def set_finished_board(self, word):
        word_list_finished = list(word)
        self.gameboard_finished = word_list_finished

    def set_create_board(self, word):
        word_list_playing = ['_'] * len(word)
        self.gameboard = word_list_playing

    def set_move(self, guess, location):
        self.gameboard[location] = guess

    def set_guess(self, player_guess):
        if player_guess in self.guess_archive:
            print("You have already tried to play " + player_guess)
        elif player_guess in self.gameboard_finished:
            for position, char in enumerate(self.gameboard_finished):
                if char == player_guess:
                    self.set_move(player_guess, position)
            self.guess_archive.append(player_guess)
        else:
            self.lives.append('x')
            self.guess_archive.append(player_guess)

    def get_eg_status(self):
        if len(self.lives) == 6:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.end_state = True 
            print("\t \t---------GAME OVER---------")
            print("Answer: \t" + ''.join(self.gameboard_finished))
            print("Thanks for playing!")

        elif self.gameboard == self.gameboard_finished:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.end_state = True
            print("\t \t---------You Won!---------")
            print("Answer: \t" + ''.join(self.gameboard_finished))
            print("Thanks for playing!")

    def get_user_guess(self):
        char = str(input("Make a guess: "))
        if len(char) == 1 and char.isalpha():
            self.set_guess(char.lower())
        else:
            print("Guess must be a single letter!")

    def set_Display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==============================================")
        print("=                  HANGMAN                   =")
        print("==============================================")
        print("\t" + ' '.join(self.gameboard))
        print("  Lives: \t" + ''.join(self.lives))
        print("Guesses: \t" + ', '.join(self.guess_archive))
        print("==============================================")
    def get_state(self):
        """Return current state info for RL agent."""
        return {
            "masked_word": ''.join(self.gameboard),
            "guessed_letters": self.guess_archive.copy(),
            "lives_left": 6 - len(self.lives),
            "end_state": self.end_state
        }

    def step(self, guess):
        """Allow RL agent to take a guess and get (new_state, reward, done)."""
        prev_lives = len(self.lives)
        prev_board = ''.join(self.gameboard)
        self.set_guess(guess)
        self.get_eg_status()
        new_board = ''.join(self.gameboard)
        done = self.end_state

        # Define rewards
        if done and self.gameboard == self.gameboard_finished:
            reward = +100
        elif done:
            reward = -100
        elif new_board != prev_board:
            reward = +10
        elif len(self.lives) > prev_lives:
            reward = -10
        else:
            reward = -1

        new_state = self.get_state()
        return new_state, reward, done


# ---------- MAIN EXECUTION ----------
# ---------- MAIN EXECUTION ----------
if __name__ == "__main__":
    game = hangman()
    game.set_Word()
    game.set_create_board(game.played_word)
    game.set_finished_board(game.played_word)
    game.set_Display()

    while not game.end_state:
        game.get_user_guess()
        game.set_Display()
        game.get_eg_status()
