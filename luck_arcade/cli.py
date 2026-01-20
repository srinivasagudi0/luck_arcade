"""
Command-line version of Luck Arcade.

Games:
- Flip a coin (easy)
- Roll a dice to hit your chosen number (medium)
- Guess a random number with difficulty levels (hard)
"""

from __future__ import annotations

import random
from typing import Iterable, Optional


MENU = """
Luck Arcade (CLI)
1. Flip a Coin (easy)
2. Roll a Dice (medium)
3. Pick a Random Number (hard)
4. Exit
"""


class QuitGame(Exception):
    """Signal to exit the CLI loop."""


def prompt_int(prompt: str, valid: Optional[Iterable[int]] = None) -> int:
    """Ask for an integer, re-prompting on bad input."""
    while True:
        raw = input(prompt).strip().lower()
        if raw in {"q", "quit", "exit"}:
            raise QuitGame
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if valid is not None and value not in valid:
            valid_list = ", ".join(str(v) for v in valid)
            print(f"Please choose one of: {valid_list}")
            continue
        return value


def prompt_yes_no(prompt: str) -> bool:
    """Return True if the user answered yes."""
    while True:
        raw = input(f"{prompt} (yes/no, q to quit): ").strip().lower()
        if raw in {"q", "quit", "exit"}:
            raise QuitGame
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("Please type yes or no.")


def flip_coin() -> None:
    print("\nWelcome to the Coin Flip Challenge! Choose your side and see if luck is on your side!\n")
    choice = prompt_int("Pick a side: 1 for Heads, 2 for Tails: ", valid={1, 2})
    chosen_side = "Heads" if choice == 1 else "Tails"
    print(f"You chose {chosen_side}. Flipping...")

    attempts = 0
    while True:
        attempts += 1
        flip = random.choice(["Heads", "Tails"])
        print(f"\n--- The coin shows {flip}! ---\n")
        if flip == chosen_side:
            print(f"Congratulations! You guessed it in {attempts} attempt(s).")
            return
        if not prompt_yes_no("No luck this time. Flip again?"):
            print(f"Stopping. The coin landed on {flip}.")
            return


def roll_dice() -> None:
    print("\nRoll a Dice — pick your lucky number and keep rolling until you hit it!\n")
    lucky_number = prompt_int("Enter your lucky number (1-6): ", valid=set(range(1, 7)))
    attempts = 0

    while True:
        attempts += 1
        roll = random.randint(1, 6)
        print(f"\n>>> You rolled a {roll}! <<<\n")
        if roll == lucky_number:
            print(f"Jackpot! You hit {lucky_number} in {attempts} attempt(s).")
            return
        if not prompt_yes_no("Missed. Roll again?"):
            print(f"Stopping. Target was {lucky_number}.")
            return


def pick_random_number() -> None:
    print("\nWelcome to the Random Number Picker! Choose a difficulty and guess the secret number.\n")
    levels = {
        1: ("Easy", 10),
        2: ("Medium", 50),
        3: ("Hard", 100),
        4: ("Nightmare", 500),
    }
    level = prompt_int("Select a level 1-4 (1=Easy, 4=Nightmare): ", valid=set(levels.keys()))
    label, max_number = levels[level]
    print(f"You picked {label}. Guess a number between 1 and {max_number}. Type q to quit.")

    target = random.randint(1, max_number)
    attempts = 0
    while True:
        try:
            guess = prompt_int(f"Your guess (1-{max_number}): ")
        except QuitGame:
            print(f"Exiting round. The number was {target}.")
            raise

        attempts += 1
        if guess == target:
            print(f"\nYOU NAILED IT! {target} was the number in {attempts} attempt(s).\n")
            return
        hint = "Too low! Aim higher." if guess < target else "Too high! Aim lower."
        print(hint)
        if not prompt_yes_no("Guess again?"):
            print(f"Better luck next time. The number was {target}.")
            return


def main() -> None:
    print("This is a luck-based game. Try your luck! Type q at any prompt to quit.\n")
    games = {"1": flip_coin, "2": roll_dice, "3": pick_random_number}

    try:
        while True:
            print(MENU)
            selection = input("Choose an option (1-4 or q): ").strip().lower()
            if selection in {"4", "q", "quit", "exit"}:
                print("Thanks for playing. Goodbye!")
                break
            func = games.get(selection)
            if func:
                try:
                    func()
                except QuitGame:
                    print("Exiting to main menu.")
            else:
                print("Please choose 1, 2, 3, or 4 to exit.")
    except QuitGame:
        print("\nThanks for playing. Goodbye!")


if __name__ == "__main__":
    main()
