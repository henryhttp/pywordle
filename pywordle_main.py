"""
    Description: Python version of the popular game Wordle, in which the user guesses
    a five character word and recieves feedback on whether or not they have guessed correct letters
    and the placement of the letters. The game ends if the user correctly guesses the word, or
    if the user uses all six allowed guesses.
"""

import random

def generate_secret_word(filepath: str) -> list[str]:
    """
        Picks a random five digit word from a given dictionary, which is located at the filepath parameter.
        Then iterates through the word and returns it as a list of the characters.
        parameters:
                :param filepath str: specified word dictionary
        return: secret_word, wordlist
    """
    secret_word: list[str] = []
    with open(filepath, "r") as f:
        wordlist = []
        for word in f:
            if len(word) == 6 and word.strip().isalpha():
                wordlist.append(word.split())
    secret_word = [letter for letter in random.choice(wordlist)[0]]
    return secret_word, wordlist

def create_user_input(wordlist: list[str]) -> list[str]:
    """
        Iterates through the user's guess to create a list of strings that matches the format of the secret_word.
        Checks for user input validity:
        - word length = 5 chars
        - alphabetical
        - exists in wordlist dictionary
        parameters:
                :param wordlist list[str]: specified word dictionary
        return: user_input
    """
    input_valid = 0
    while input_valid < 2:
        user_input = [letter for letter in str(input("Enter a guess: "))]
        if not any(''.join(user_input) == word[0] for word in wordlist):
            print("That is not a five-letter word in our dictionary.")
        else:
            input_valid += 1
        if not(all(char.isalpha() for char in user_input) and len(user_input) == 5):
            print("Error: Guesses must be five characters and alphabetical.")
        else:
            input_valid += 1
    return user_input

def print_yellow(s, end='\n'):
   print('\u001b[43;1m', end='')
   print(s, end=end)
   print('\033[0m', end='')

def print_grey(s, end='\n'):
   print('\u001b[47;1m', end='')
   print(s, end=end)
   print('\033[0m', end='')



def check_guess(guess: list[str], secret_word: list[str]) -> str:
    """
        Checks if the user's guess contains letters in the exact position or at all in the secret code.
        Method:
        - Makes a copy of the guess to modify in order to exclude duplicates.
        - Creates a relfected guess to output that contains information about the guesses correctness.
        - Checks all letter indexes for exact positions, then excludes those letters from being checked again.
        - Repeats process for correct letters being in the secret code at all.
        - Handles guess history and guess counts, ends game if guess count is 6 and guess is incorrect.
        - Prints previous guesses with colors for user intel on next guess.

        parameters:
                :param guess list[str]: guess stored as a list of characters
                :param guess secret_word[str]: secret word stored as list of characters
        return: None
    """
    modify_guess = guess.copy()
    reflected_guess = ["\033[97m" + letter.capitalize() + "\033[00m " for letter in guess]

    correct_positions = []
    correct_letters = []
    misplaced_count = {}

    for l_index, l_value in enumerate(modify_guess):
        if modify_guess[l_index] == secret_word[l_index]:
            modify_guess[l_index] = '0'
            reflected_guess[l_index] = "\033[92m" + guess[l_index].capitalize() + "\033[00m "  # green text
            correct_positions.append(l_index)
            correct_letters.append(secret_word[l_index])

    for l_index, l_value in enumerate(modify_guess):
        if (
            modify_guess[l_index] != '0' and
            modify_guess[l_index] in secret_word and
            l_index not in correct_positions and
            secret_word[l_index] not in correct_letters
        ):
            if modify_guess[l_index] not in misplaced_count:
                misplaced_count[modify_guess[l_index]] = 1
            else:
                misplaced_count[modify_guess[l_index]] += 1

            if misplaced_count[modify_guess[l_index]] <= secret_word.count(modify_guess[l_index]):
                modify_guess[l_index] = '1'
                reflected_guess[l_index] = "\033[93m" + guess[l_index].capitalize() + "\033[00m "  # yellow text

    guess_history.append([guess_count, guess, reflected_guess])
    
    for guess_index, guess_value in enumerate(guess_history):
        print(f"Guess {guess_history[guess_index][0]}: {''.join(guess_history[guess_index][2])}")

    if guess_count == 6 and guess != secret_word:
        print("You lose, you did not guess the word in 6 guesses.")
        exit()

def main():
    global wordlist, guess_count, guess_history, secret_word

    secret_word, wordlist = generate_secret_word("usaWords.txt")
    guess_count = 0
    guess_history = []
    guess = []

    print("Welcome to Wordle! You have six chances to guess the five-letter word.\nA green letter means you got that letter correct and in the right position.\nA yellow letter means you matched that letter, but it is in the wrong position.\nA white letter means that letter does not appear in the correct word.")
    while guess != secret_word:
        guess = create_user_input(wordlist)
        guess_count += 1
        check_guess(guess, secret_word)
    print(f"You win. You got it in {len(guess_history)} guesses.")
    exit()

if __name__ == "__main__":
    main()