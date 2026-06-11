from solution import run_length_encode

def test_basic():
    assert run_length_encode("aabbbcc") == [("a", 2), ("b", 3), ("c", 2)]

def test_empty():
    assert run_length_encode("") == []

def test_no_repeats():
    assert run_length_encode("abc") == [("a", 1), ("b", 1), ("c", 1)]

def test_single_char_repeated():
    assert run_length_encode("aaaa") == [("a", 4)]

def test_single_char():
    assert run_length_encode("z") == [("z", 1)]
