import string                                                               
import os                                                                   # Used for clearing the term window
import time                                                                 # Used for 5 second buffer at the end of the game
import random                                                               # To pick random word from list

class hangman:
    # Var
    played_word = ""                                                        # Word in play
    gameboard = []                                                          # Playing game board
    gameboard_finished = []                                                 # End-State game board
    guess = ''                                                              # Guess that's made
    guess_archieve = []                                                     # Creates list of all guesses
    lives = []                                                              # Players life count
    end_state = False                                                       # Is the game over
    # List create from random word generator
    word_list = ['stun','amuse','comment','systematic','adviser','argument','chemistry','ward','goal','knot','confession','desk','opinion','dilute','horoscope','number','overall','dark','girl','association','reserve','shrink','autonomy','worker','confrontation','mountain','conception','corpse','prestige','family','belief','mobile','trouble','temptation']
 

    def set_Word(self):
        word = random.choice(self.word_list)                                # Using random to grab random word from word_list
        self.played_word = word

    def set_finished_board(self,word):
        word_list_finished = list(word)
        self.gameboard_finished = word_list_finished

    def set_create_board(self,word):
        word_list_playing = ['_'] * len(word)
        self.gameboard = word_list_playing

    def set_move(self,guess,location):
        self.gameboard[location] = guess

    def set_guess(self,player_guess):
        if(player_guess in self.guess_archieve):                            # Check if guess has already been made
            print("You have already tried to play " + player_guess)    
        elif(player_guess in self.gameboard_finished):                      # Checking if guess is in found in gameboard_finished
            for position,char in enumerate(self.gameboard_finished):
                if char== player_guess:                                     # Checks for all chances of the guess within gameboard_finished
                    self.set_move(self,player_guess,position)
            self.guess_archieve.append(player_guess)
        else:
            self.lives.append('x')                                          # Add x to lives
            self.guess_archieve.append(player_guess)                    


    def get_eg_status(self):
        if(len(self.lives) == 5):
            os.system('cls' if os.name == 'nt' else 'clear')                # Clear term
            self.end_state = True
            print("\t \t---------GAME OVER---------")
            print("Answer: \t" + str(self.gameboard_finished))
            print("Thanks for playing! Game will close in 5 secounds!")
            time.sleep(5)
        elif(self.gameboard == self.gameboard_finished):
            os.system('cls' if os.name == 'nt' else 'clear')                # Clear term
            self.end_state = True
            print("\t \t---------You Won!---------")
            print("Answer: \t" + str(self.gameboard_finished))
            print("Thanks for playing! Game will close in 5 secounds!")
            time.sleep(5)

    def get_user_guess(self):
        char = str(input("Make a guess: "))
        if(len(char) == 1 and char.isalpha()):
            self.set_guess(self,char.lower())
        else:
            print("Guess must be a single letter!")
            
    def set_Display(self):
            os.system('cls' if os.name == 'nt' else 'clear')                # Clear Term
            # DEBUG Game Board Display
            print("==============================================")
            print("=                  HANGMAN                   =")
            print("==============================================")
            print("\t" + str(self.gameboard))
            print("  Lives: \t" + str(game.lives))
            print("Guesses: \t" + str(self.guess_archieve))
            print("============================================== ")



game = hangman                                                              # Create Game Object
game.set_Word(game)                                                         # Word in play
game.set_create_board(game,game.played_word)                                # game board
game.set_finished_board(game,game.played_word)                              # end-state 
game.set_Display(game)                                                      # Show board for the first time

while(game.end_state != True):
    game.get_user_guess(game)                                               # Get input(guess) from user
    game.set_Display(game)                                                  # Display Updated Board 
    game.get_eg_status(game)                                                # Check End-Game Status
    