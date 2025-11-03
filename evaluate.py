import os
import json
import pickle
from hangman import hangman
from rl_agent import RLAgent
from hmm_model import HMM


def evaluate_agent_on_test(agent, hmm, test_file="Data/test.txt", save_results=True):
    total_words = 0
    correct_words = 0
    incorrect_words = 0

    # Load test words
    with open(test_file, "r") as f:
        words = [line.strip().lower() for line in f.readlines() if line.strip()]

    print("\n🧠 Starting Evaluation on Test Data...\n")

    for word in words:
        total_words += 1
        game = hangman()
        game.reset()
        game.played_word = word
        game.set_finished_board(word)
        game.set_create_board(word)

        done = False
        while not done:
            masked = ''.join(game.gameboard)
            guessed = game.guess_archive.copy()
            hmm_probs = hmm.get_letter_probs(masked, guessed)
            action = agent.select_action(masked, guessed, hmm_probs)
            _, _, done = game.step(action)

        #Check if the agent successfully guessed the word
        if game.gameboard == game.gameboard_finished:
            correct_words += 1
            #print(f"✅ {word.upper()}  — Guessed correctly!")
        else:
            incorrect_words += 1
            #print(f"❌ {word.upper()}  — Failed (lives exhausted or incorrect guesses)")

    # Compute accuracy
    accuracy = (correct_words / total_words) * 100 if total_words else 0

    print("\n📊 FINAL EVALUATION RESULTS 📊")
    print(f"Total Words Tested: {total_words}")
    print(f"Correctly Guessed:  {correct_words}")
    print(f"Incorrect Words:    {incorrect_words}")
    print(f"Accuracy:           {accuracy:.2f}%")

    # Save results
    if save_results:
        os.makedirs("results", exist_ok=True)
        results = {
            "total_words": total_words,
            "correct_words": correct_words,
            "incorrect_words": incorrect_words,
            "accuracy": accuracy
        }
        with open("results/evaluation_summary.json", "w") as f:
            json.dump(results, f, indent=4)
        print("\n📝 Results saved to results/evaluation_summary.json")

    return accuracy


if __name__ == "__main__":
    print("\n🎯 EVALUATION MODE ACTIVE 🎯")

    # Load HMM trained on corpus
    hmm = HMM("Data/corpus.txt")

    # Initialize RL Agent
    agent = RLAgent(epsilon=0)  # No randomness during testing

    # 🔹 Load the trained Q-table (saved after training)
    qtable_path = "results/trained_qtable.pkl"
    if os.path.exists(qtable_path):
        with open(qtable_path, "rb") as f:
            agent.Q = pickle.load(f)
        print(f"✅ Loaded trained Q-table with {len(agent.Q)} entries from {qtable_path}")
    else:
        print(f"⚠️ Warning: Trained Q-table not found at {qtable_path}. Running untrained agent.")

    # 🔹 Run evaluation
    accuracy = evaluate_agent_on_test(agent, hmm, "Data/test.txt")
    print(f"\n✅ Model Accuracy on Test Set: {accuracy:.2f}%")
