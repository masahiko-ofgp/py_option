import pytest
from src.py_option import Option, OptionType

s = Option.new(123)
sn = Option.new(Option.new())
answer = Option.new(444)
n = Option.new()

def test_compare_some_and_non():
    assert s == s
    assert n == n
    assert s != n
    assert n != s

def test_is_some():
    assert Option.is_some(s) is True
    assert Option.is_some(n) is False

def test_is_non():
    assert Option.is_non(n) is True
    assert Option.is_non(s) is False

def test_expect():
    e = Option.expect(s, "Not Some")
    assert e == 123

    with pytest.raises(TypeError):
        Option.expect(n, "This is Non")

def test_unwrap():
    assert Option.unwrap(s) == 123

    with pytest.raises(TypeError):
        Option.unwrap(n)

def test_unwrap_or():
    assert Option.unwrap_or(s, 0) == 123
    assert Option.unwrap_or(n, 0) == 0

def test_unwrap_or_else():
    assert Option.unwrap_or_else(s, lambda : "Hello") == 123
    assert Option.unwrap_or_else(n, lambda: "Hello") == "Hello"

def test_map():
    assert Option.map(s, lambda x: x + 321) == answer

    with pytest.raises(TypeError):
        Option.map(n, lambda x: x + 321)

    with pytest.raises(TypeError):
        Option.map(sn, lambda x: x + 321)

def test_map_or():
    assert Option.map_or(s, 0, lambda x: x + 321) == answer
    assert Option.map_or(n, 0, lambda x: x + 321) == 0
    assert Option.map_or(sn, 0, lambda x: x + 321) == 0

def test_map_or_else():
    assert Option.map_or_else(s, lambda: "Hello", lambda x: x + 321) == answer
    assert Option.map_or_else(n, lambda: "Hello", lambda x: x + 321) == "Hello"
    assert Option.map_or_else(sn, lambda: "Hello", lambda x: x + 321) == "Hello"

def test_and_option():
    assert Option.and_option(n, s) == n
    assert Option.and_option(s, n) == n
    assert Option.and_option(s, sn) == sn

def test_and_then():
    assert Option.and_then(s, lambda x: x + 321) == answer
    assert Option.and_then(n, lambda x: x + 321) == n
    with pytest.raises(TypeError):
        Option.and_then(s, lambda x: x + "Hello")
    with pytest.raises(TypeError):
        Option.and_then(sn, lambda x: x + 321)

def test_zip():
    s2 = Option.new("Hello")
    assert Option.zip(s, s2) == (OptionType.Some, (123, 'Hello'))
    assert Option.zip(s, n) == (OptionType.Non,)
    assert Option.zip(n, s) == (OptionType.Non,)
    with pytest.raises(TypeError):
        Option.zip(s2, "world")
