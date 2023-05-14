from logic_test_1 import fizz_buzz
from logic_test_2 import fibonacci
from logic_test_3 import words_repetitions


def test_logic_test_1():
    for n in range(1, 101):
        if (n % 3 == 0) and (n % 5 == 0):
            assert fizz_buzz(n) == 'fizz buzz'
        elif (n % 5 == 0):
            assert fizz_buzz(n) == 'buzz'
        elif (n % 3 == 0):
            assert fizz_buzz(n) == 'fizz'
        else:
            assert fizz_buzz(n) == str(n)


def test_logic_test_2():
    """pytest"""
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(2) == 1
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55
    assert fibonacci(15) == 610


def test_logic_test_3():
    """pytest"""
    sample_text = "Hi how are things? How are you? Are you a developer? I am also a developer"
    expected_result = {'hi': 1, 'how': 2, 'are': 3, 'things': 1, 'you': 2, 'a': 2, 'developer': 2, 'i': 1, 'am': 1, 'also': 1}
    assert words_repetitions(sample_text) == expected_result
