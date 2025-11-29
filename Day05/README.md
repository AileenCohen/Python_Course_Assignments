# Classic Hangman Game

An ASCII-based implementation of the classic word-guessing game "Hangman". 

## What is Hangman?

Hangman is a game where a player tries to guess a hidden word, one letter at a time.

If the letter is in the word, it is shown.

If the letter is not in the word, a part of a "hangman" stick figure is drawn.

The game ends when the word is guessed or the drawing is complete (6 mistakes).


## Folder Structure

**hangman_logic.py**

The Brain. Contains pure functions for checking guesses, updating state, and determining win/loss conditions. No print() calls here.

**hangman_app.py**

The Face. Handles user input, displays the ASCII art, and runs the main game loop.

**test_hangman.py**

The Verifier. Contains pytest unit tests to ensure the logic functions work correctly without playing the game manually.

## How to Run

1. Start the Game

Run the application file to start playing:
```
python hangman_app.py
```

2. Run the Tests

To verify that the game logic (input validation, win checking) works as expected:
```
pytest
```

## AI Usage:
### AI used:
Github Copilot
Gemini

### Prompts:
- For github copilot:
Write a .github/copilot-instructions.md file that fits my project folder.

- For Gemini:
Write the tests for the hangman game.