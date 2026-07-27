
"""
Task 4: Rock-Paper-Scissors Game
User plays against the computer, with score tracking across multiple rounds.
"""

import random

CHOICES = ["rock", "paper", "scissors"]

# Maps each choice to the choice it beats
BEATS = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock",
}


def get_user_choice():
    """Prompt the user until they enter a valid choice."""
    while True:
        choice = input("Choose rock, paper, or scissors: ").strip().lower()
        if choice in CHOICES:
            return choice
        print("Invalid choice. Please type rock, paper, or scissors.")


def get_computer_choice():
    """Randomly select rock, paper, or scissors for the computer."""
    return random.choice(CHOICES)


def determine_winner(user_choice, computer_choice):
    """Return 'user', 'computer', or 'tie' based on game rules."""
    if user_choice == computer_choice:
        return "tie"
    if BEATS[user_choice] == computer_choice:
        return "user"
    return "computer"


def play_round(scores):
    """Play a single round and update the scores dict in place."""
    user_choice = get_user_choice()
    computer_choice = get_computer_choice()

    print(f"\nYou chose: {user_choice}")
    print(f"Computer chose: {computer_choice}")

    result = determine_winner(user_choice, computer_choice)

    if result == "tie":
        print("It's a tie!\n")
    elif result == "user":
        print("You win this round!\n")
        scores["user"] += 1
    else:
        print("Computer wins this round!\n")
        scores["computer"] += 1


def ask_play_again():
    while True:
        choice = input("Play again? (y/n): ").strip().lower()
        if choice in ("y", "yes"):
            return True
        
        if choice in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def main():
    print("=== Rock, Paper, Scissors ===\n")
    scores = {"user": 0, "computer": 0}

    while True:
        play_round(scores)
        print(f"Score -> You: {scores['user']}  Computer: {scores['computer']}\n")

        if not ask_play_again():
            break

    print("\nFinal Score:")
    print(f"You: {scores['user']}  Computer: {scores['computer']}")

    if scores["user"] > scores["computer"]:
        print("Congratulations, you won overall!")
    elif scores["user"] < scores["computer"]:
        print("Computer won overall. Better luck next time!")
    else:
        print("Overall, it's a tie!")

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()