import pytest
from src.py_option import Option, Some, Non

s = Some(123)
sn = Some(Non)
n = Non()

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

    with pytest.raises(ValueError):
        Option.expect(n, "This is Non")

def test_unwrap():
    assert Option.unwrap(s) == 123
    
    with pytest.raises(ValueError):
        Option.unwrap(n)

def test_unwrap_or():
    assert Option.unwrap_or(s, 0) == 123
    assert Option.unwrap_or(n, 0) == 0

def test_unwrap_or_else():
    assert Option.unwrap_or_else(s, lambda : "Hello") == 123
    assert Option.unwrap_or_else(n, lambda: "Hello") == "Hello"

def test_map():
    assert Option.map(s, lambda x: x + 321) == Some(444)

    with pytest.raises(ValueError):
        Option.map(n, lambda x: x + 321) 

    with pytest.raises(ValueError):
        Option.map(sn, lambda x: x + 321)
        
def test_map_or():
    assert Option.map_or(s, 0, lambda x: x + 321) == Some(444)
    assert Option.map_or(n, 0, lambda x: x + 321) == 0

    with pytest.raises(ValueError):
        Option.map_or(sn, 0, lambda x: x + 321)
        
def test_map_or_else():
    assert Option.map_or_else(s, lambda: "Hello", lambda x: x + 321) == Some(444)
    assert Option.map_or_else(n, lambda: "Hello", lambda x: x + 321) == "Hello"

    with pytest.raises(ValueError):
        Option.map_or_else(sn, lambda: "Hello", lambda x: x + 321)
        
