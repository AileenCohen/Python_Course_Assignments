import hangman_logic


HANGMAN_ASCII_ART = """Welcome to the game Hangman
  _    _
 | |  | |
 | |__| | __ _ _ __    __ _ _ __ ___    __ _ _ __
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |
                     |___/
"""

HANGMAN_PHOTOS = {
    1: "  x-------x\n",
    2: """      x-------x
      |
      |
      |
      |
      |\n""",
    3: """      x-------x
      |        |
      |        0
      |
      |
      |\n""",
    4: """      x-------x
      |        |
      |        0
      |        |
      |
      |\n""",
    5: """      x-------x
      |        |
      |        0
      |      /|\\
      |
      |\n""",
    6: """      x-------x
      |        |
      |        0
      |      /|\\
      |      /
      |\n""",
    7: """      x-------x
      |        |
      |        0
      |      /|\\
      |      / \\
      |\n"""
}


def start_game():
    """Returns the welcome art."""
    return HANGMAN_ASCII_ART

def print_hangman(num_of_tries):
    """Returns the color-coded hangman picture based on mistakes."""
    if num_of_tries == 0:
        return "\n" + "Let's start!\n" + "\n" + '\033[36m' + HANGMAN_PHOTOS[num_of_tries + 1] + '\033[0m'
    if num_of_tries <= 2:
        return "\n" + '\033[32m' + HANGMAN_PHOTOS[num_of_tries + 1] + '\033[0m'
    if num_of_tries <= 5:
        return "\n" + '\033[35m' + HANGMAN_PHOTOS[num_of_tries + 1] + '\033[0m'
    if num_of_tries == 6:
        return "\n" + '\033[31m' + HANGMAN_PHOTOS[num_of_tries + 1] + '\033[0m'
    return ""

def main():
    print(start_game())
    MAX_TRIES = 6
    num_of_tries = 0
    print('The number of tries you have: ', MAX_TRIES)

    secret_word = hangman_logic.choose_word()
    
    print(print_hangman(num_of_tries))
    old_letters_guessed = []
    print("_ " * len(secret_word))

    while num_of_tries < MAX_TRIES:
        letter_guessed = input('Guess a letter: ')


        if not hangman_logic.try_update_letter_guessed(letter_guessed, old_letters_guessed):
            print("X")
            old_letters_guessed.sort()
            print("->".join(old_letters_guessed))
            continue

        # Check guess against logic
        if letter_guessed.lower() in secret_word:
            print(hangman_logic.show_hidden_word(secret_word, old_letters_guessed))
            
            if hangman_logic.check_win(secret_word, old_letters_guessed):
                print("WIN")
                break
        else:
            num_of_tries += 1
            print(":(\n" + print_hangman(num_of_tries))
            print(hangman_logic.show_hidden_word(secret_word, old_letters_guessed))

    if not hangman_logic.check_win(secret_word, old_letters_guessed):
        print("LOSE")
        print(f"The secret word was: **{secret_word}**")

if __name__ == "__main__":
    main()