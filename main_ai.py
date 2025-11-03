import os
import time
from hangman import hangman
from rl_agent import RLAgent
from hmm_model import HMM

def run_ai_games(num_games=5, sleep_time=1.0):
    hmm = HMM("Data/corpus.txt")
    agent = RLAgent(epsilon=0)  # no randomness, pure strategy

    for game_num in range(1, num_games + 1):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"================= GAME {game_num} =================")
        game = hangman()
        game.set_Word()
        game.set_finished_board(game.played_word)
        game.set_create_board(game.played_word)

        state = game.get_state()
        done = False
        total_reward = 0

        while not done:
            masked = state["masked_word"]
            guessed = state["guessed_letters"]
            hmm_probs = hmm.get_letter_probs(masked, guessed)

            # Agent chooses letter
            action = agent.select_action(masked, guessed, hmm_probs)
            next_state, reward, done = game.step(action)

            # RL update (optional here since we're just watching)
            s_key = agent._encode_state(masked, guessed)
            s_next = agent._encode_state(next_state["masked_word"], next_state["guessed_letters"])
            agent.update(s_key, action, reward, s_next)

            total_reward += reward

            # Display gameboard
            os.system('cls' if os.name == 'nt' else 'clear')
            print("==============================================")
            print("=                  HANGMAN                   =")
            print("==============================================")
            print("\t" + ' '.join(game.gameboard))
            print("  Lives: \t" + ''.join(game.lives))
            print("Guesses: \t" + ', '.join(game.guess_archive))
            print("==============================================")
            print(f"Agent guessed: '{action.upper()}' | Reward: {reward}")
            time.sleep(sleep_time)

            state = next_state

        print(f"\n✅ Game {game_num} finished! Word was: {game.played_word}")
        print(f"Total Reward: {total_reward}")
        time.sleep(2.5)
def evaluate_agent_on_test(agent, hmm, test_file="Data/test.txt"):
    total_words = 0
    correct_words = 0
    total_wrong_guesses = 0
    total_repeated_guesses = 0
    total_score = 0

    with open(test_file, "r") as f:
        words = [line.strip().lower() for line in f.readlines() if line.strip()]

    print("\n🧠 Starting Evaluation on Test Data...\n")

    for word in words:
        total_words += 1
        game = hangman()
        game.played_word = word
        # game.set_finished_board(word)
        # game.set_create_board(word)
        # game.guess_archive = []
        # game.lives = []
        # game.guess = ''
        # game.guess_archive = []       
        # state = game.get_state()
        # done = False
        wrong_guesses = 0
        # repeated_guesses = 0

        while not done:
            masked = state["masked_word"]
            guessed = state["guessed_letters"]
            hmm_probs = hmm.get_letter_probs(masked, guessed)
            action = agent.select_action(masked, guessed, hmm_probs)

            if action in guessed:
                repeated_guesses += 1

            next_state, reward, done = game.step(action)
            if reward == -10:
                wrong_guesses += 1
            state = next_state

        # Count success
        if game.gameboard == game.gameboard_finished:
            correct_words += 1
        del game
    # Scoring formula
    total_score += (2000 * int(game.gameboard == game.gameboard_finished)) - (5 * wrong_guesses) - (2 * repeated_guesses)
    total_wrong_guesses += wrong_guesses
    total_repeated_guesses += repeated_guesses

    # Final metrics
    accuracy = (correct_words / total_words) * 100
    avg_wrong = total_wrong_guesses / total_words
    avg_repeat = total_repeated_guesses / total_words

    print("\n📊 EVALUATION RESULTS 📊")
    print(f"Total Words Tested:      {total_words}")
    print(f"Correctly Guessed:       {correct_words}")
    print(f"Accuracy:                {accuracy:.2f}%")
    print(f"Average Wrong Guesses:   {avg_wrong:.2f}")
    print(f"Average Repeated Letters:{avg_repeat:.2f}")
    print(f"Final Score:             {total_score}")

    return {
        "accuracy": accuracy,
        "score": total_score,
        "wrong_guesses": total_wrong_guesses,
        "repeats": total_repeated_guesses
    }

if __name__ == "__main__":
    run_ai_games(num_games=5, sleep_time=1.0)
