import pytest
from hangman_logic import check_valid_input, try_update_letter_guessed, show_hidden_word, check_win

class TestHangmanLogic:

    def test_check_valid_input_valid_letter(self):
        """Test that a single alphabetic character that hasn't been guessed is valid."""
        old_guesses = ['a', 'b']
        assert check_valid_input('c', old_guesses) is True

    def test_check_valid_input_invalid_length(self):
        """Test that input with length != 1 is invalid."""
        old_guesses = ['a', 'b']
        assert check_valid_input('cc', old_guesses) is False
        assert check_valid_input('', old_guesses) is False

    def test_check_valid_input_non_alpha(self):
        """Test that non-alphabetic characters are invalid."""
        old_guesses = ['a', 'b']
        assert check_valid_input('$', old_guesses) is False
        assert check_valid_input('1', old_guesses) is False

    def test_check_valid_input_already_guessed(self):
        """Test that a letter already in the guessed list is invalid."""
        old_guesses = ['a', 'b', 'c']
        assert check_valid_input('a', old_guesses) is False
        assert check_valid_input('A', old_guesses) is False

    def test_try_update_success(self):
        """Test that a valid letter is added to the list and returns True."""
        old_guesses = ['a', 'b']
        result = try_update_letter_guessed('c', old_guesses)
        
        assert result is True
        assert 'c' in old_guesses
        assert len(old_guesses) == 3

    def test_try_update_fail_invalid(self):
        """Test that an invalid letter is NOT added and returns False."""
        old_guesses = ['a', 'b']
        original_len = len(old_guesses)
        result = try_update_letter_guessed('1', old_guesses)
        
        assert result is False
        assert len(old_guesses) == original_len

    def test_try_update_fail_duplicate(self):
        """Test that a duplicate letter is NOT added again and returns False."""
        old_guesses = ['a', 'b']
        original_len = len(old_guesses)
        result = try_update_letter_guessed('a', old_guesses)
        
        assert result is False
        assert len(old_guesses) == original_len


    def test_show_hidden_word_all_hidden(self):
        """Test display when no letters have been guessed."""
        secret_word = "mammoth"
        old_guesses = ['b', 'c']
        expected = "_ _ _ _ _ _ _"
        assert show_hidden_word(secret_word, old_guesses) == expected

    def test_show_hidden_word_partial_reveal(self):
        """Test display with some correct guesses."""
        secret_word = "mammoth"
        old_guesses = ['m', 't']
        expected = "m _ m m _ t _"
        assert show_hidden_word(secret_word, old_guesses) == expected

    def test_show_hidden_word_full_reveal(self):
        """Test display when all letters are guessed."""
        secret_word = "cat"
        old_guesses = ['c', 'a', 't', 'z']
        expected = "c a t"
        assert show_hidden_word(secret_word, old_guesses) == expected

    def test_check_win_true(self):
        """Test that check_win returns True when all secret letters are in guesses."""
        secret_word = "dog"
        old_guesses = ['d', 'o', 'g', 's']
        assert check_win(secret_word, old_guesses) is True

    def test_check_win_false(self):
        """Test that check_win returns False when letters are missing."""
        secret_word = "dog"
        old_guesses = ['d', 'o']
        assert check_win(secret_word, old_guesses) is False