import random

WORD_POOL = [
    "python", "hangman", "programming", "computer", "algorithm",
    "developer", "keyboard", "monitor", "software", "hardware",
    "internet", "variable", "function", "integer", "string",
    "boolean", "iterate", "recursion", "module", "library",
    "framework", "database", "security", "network", "protocol",
    "machine", "learning", "artificial", "intelligence", "webpage",
    "javascript", "html", "cascade", "style", "server",
    "client", "cloud", "storage", "encryption", "debugging",
    "testing", "deploy", "version", "control", "repository",
    "git", "linux", "windows", "macos", "terminal"
]



def choose_word():
    return random.choice(WORD_POOL)

def check_valid_input(letter_guessed, old_letters_guessed):
    letter_guessed = letter_guessed.lower()
    if len(letter_guessed) != 1:
        return False
    if not letter_guessed.isalpha():
        return False
    if letter_guessed in old_letters_guessed:
        return False
    return True

def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    letter_guessed = letter_guessed.lower()
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed)
        return True
    return False

def show_hidden_word(secret_word, old_letters_guessed):
    result = []
    for char in secret_word:
        if char in old_letters_guessed:
            result.append(char)
        else:
            result.append("_")
    return " ".join(result)

def check_win(secret_word, old_letters_guessed):
    current_state = show_hidden_word(secret_word, old_letters_guessed).replace(" ", "")
    return current_state == secret_word