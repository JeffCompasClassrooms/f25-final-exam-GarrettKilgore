import pytest
from unittest.mock import Mock, patch, call
from brute import Brute

def describe_bruteOnce():
    
    def it_returns_true_when_attempt_matches_password():
        password = "test123"
        brute = Brute(password)
        assert brute.bruteOnce(password) == True
    
    def it_returns_false_when_attempt_does_not_match():
        password = "secret"
        brute = Brute(password)
        assert brute.bruteOnce("wrong") == False
    
    def it_is_case_sensitive():
        password = "TestPass"
        brute = Brute(password)
        assert brute.bruteOnce("TestPass") == True
        assert brute.bruteOnce("testpass") == False
        assert brute.bruteOnce("TESTPASS") == False
    
    def it_handles_single_character_passwords():
        password = "a"
        brute = Brute(password)
        assert brute.bruteOnce("a") == True
        assert brute.bruteOnce("b") == False
    
    def it_handles_maximum_length_passwords():
        password = "abcd1234"
        brute = Brute(password)
        assert brute.bruteOnce("abcd1234") == True
        assert brute.bruteOnce("abcd123") == False
    
    def it_handles_numeric_only_passwords():
        password = "12345"
        brute = Brute(password)
        assert brute.bruteOnce("12345") == True
        assert brute.bruteOnce("54321") == False
    
    def it_handles_alphabetic_only_passwords():
        password = "abcdef"
        brute = Brute(password)
        assert brute.bruteOnce("abcdef") == True
        assert brute.bruteOnce("fedcba") == False
    
    def it_handles_mixed_case_alphanumeric():
        password = "Abc123"
        brute = Brute(password)
        assert brute.bruteOnce("Abc123") == True
        assert brute.bruteOnce("abc123") == False
    
    def it_handles_empty_string_attempt():
        password = "test"
        brute = Brute(password)
        assert brute.bruteOnce("") == False
    
    def it_handles_empty_string_password():
        password = ""
        brute = Brute(password)
        assert brute.bruteOnce("") == True
        assert brute.bruteOnce("a") == False


def describe_bruteMany():
    
    def it_returns_positive_time_when_password_is_cracked_success():
        password = "test"
        brute = Brute(password)
        with patch.object(brute, 'randomGuess', side_effect=["wrong1", "wrong2", password]):
            result = brute.bruteMany(limit=100)
            assert result >= 0
            assert isinstance(result, float)
    
    def it_returns_negative_one_when_limit_exceeded_failure():
        password = "impossible"
        brute = Brute(password)
        with patch.object(brute, 'randomGuess', return_value="wrong"):
            result = brute.bruteMany(limit=10)
            assert result == -1
    
    def it_respects_the_limit_parameter():
        password = "test"
        brute = Brute(password)
        mock_guess = Mock(return_value="wrong")
        with patch.object(brute, 'randomGuess', mock_guess):
            result = brute.bruteMany(limit=50)
            assert mock_guess.call_count == 50
            assert result == -1
    
    def it_uses_default_limit_when_not_specified():
        password = "test"
        brute = Brute(password)
        guesses = ["wrong"] * 99 + [password]
        with patch.object(brute, 'randomGuess', side_effect=guesses):
            result = brute.bruteMany()
            assert result >= 0
    
    def it_calls_randomGuess_for_each_attempt():
        password = "abc"
        brute = Brute(password)
        mock_guess = Mock(side_effect=["xyz", "def", password])
        with patch.object(brute, 'randomGuess', mock_guess):
            result = brute.bruteMany(limit=10)
            assert mock_guess.call_count == 3
            assert result >= 0
    
    def it_calls_bruteOnce_with_each_random_guess():
        password = "test"
        brute = Brute(password)
        guesses = ["a", "b", "c", password]
        with patch.object(brute, 'randomGuess', side_effect=guesses):
            mock_bruteOnce = Mock(side_effect=[False, False, False, True])
            with patch.object(brute, 'bruteOnce', mock_bruteOnce):
                result = brute.bruteMany(limit=10)
                expected_calls = [call("a"), call("b"), call("c"), call(password)]
                mock_bruteOnce.assert_has_calls(expected_calls)
                assert mock_bruteOnce.call_count == 4
    
    def it_stops_immediately_on_first_match():
        password = "test"
        brute = Brute(password)
        mock_guess = Mock(side_effect=["a", "b", "c", "d", password, "should_not_reach"])
        with patch.object(brute, 'randomGuess', mock_guess):
            result = brute.bruteMany(limit=100)
            assert mock_guess.call_count == 5
            assert result >= 0
    
    def it_measures_elapsed_time_correctly():
        password = "x"
        brute = Brute(password)
        with patch.object(brute, 'randomGuess', side_effect=["a", "b", password]):
            result = brute.bruteMany(limit=100)
            assert result >= 0
            assert result < 1
            
    def it_handles_edge_case_limit_of_one():
        password = "test"
        brute = Brute(password)
        mock_guess = Mock(return_value="wrong")
        with patch.object(brute, 'randomGuess', mock_guess):
            result = brute.bruteMany(limit=1)
            assert result == -1
            assert mock_guess.call_count == 1
    
    def it_handles_edge_case_limit_of_zero():
        password = "test"
        brute = Brute(password)
        mock_guess = Mock(return_value="test")
        with patch.object(brute, 'randomGuess', mock_guess):
            result = brute.bruteMany(limit=0)
            assert result == -1
            assert mock_guess.call_count == 0
    
    def it_succeeds_on_first_attempt():
        password = "z"
        brute = Brute(password)
        mock_guess = Mock(side_effect=[password])
        with patch.object(brute, 'randomGuess', mock_guess):
            result = brute.bruteMany(limit=100)
            assert result >= 0
            assert mock_guess.call_count == 1
    
    def it_uses_hash_method_for_comparison():
        password = "test"
        brute = Brute(password)
        original_hash = brute.hash
        mock_hash = Mock(side_effect=lambda s: original_hash(s))
        with patch.object(brute, 'hash', mock_hash):
            with patch.object(brute, 'randomGuess', side_effect=["a", password]):
                result = brute.bruteMany(limit=10)
                assert mock_hash.call_count >= 2
                assert result >= 0
    
    def it_handles_single_character_password_success():
        password = "a"
        brute = Brute(password)
        with patch.object(brute, 'randomGuess', side_effect=["x", "y", "z", password]):
            result = brute.bruteMany(limit=100)
            assert result >= 0
    
    def it_handles_maximum_length_password_success():
        password = "abcd1234"
        brute = Brute(password)
        with patch.object(brute, 'randomGuess', side_effect=["wrong", password]):
            result = brute.bruteMany(limit=100)
            assert result >= 0
    
    def it_handles_empty_password_edge_case():
        password = ""
        brute = Brute(password)
        with patch.object(brute, 'randomGuess', side_effect=["a", ""]):
            result = brute.bruteMany(limit=100)
            assert result >= 0