from py_option import Option, OptionTypeError
import pytest


s = Option.new(123)
n = Option.new()

ss = Option.new(s)
sn = Option.new(n)


def test_is_some():
    assert s.is_some()
    assert not n.is_some()
    assert ss.is_some()
    assert sn.is_some()


def test_is_some_and():
    assert s.is_some_and(lambda x: x) == 123
    assert n.is_some_and(lambda x: x) is False
    assert ss.is_some_and(lambda x: x) == s
    assert sn.is_some_and(lambda x: x) == n


def test_is_non():
    assert not s.is_non()
    assert n.is_non()
    assert not ss.is_non()
    assert not sn.is_non()


def test_expect():
    assert s.expect("Panic!!") == 123

    with pytest.raises(OptionTypeError, match="Panic!!"):
        n.expect("Panic!!")

    assert ss.expect("Panic!!") == s
    assert sn.expect("Panic!!") == n


def test_filter():
    assert s.filter(lambda x: x % 2 == 0) == n
    assert s.filter(lambda x: x % 2 == 1) == s
    assert n.filter(lambda x: x % 2 == 0) == n

    with pytest.raises(TypeError):
        ss.filter(lambda x: x % 2 == 0)

    with pytest.raises(TypeError):
        sn.filter(lambda x: x % 2 == 0)


def test_unwrap():
    pass


def test_unwrap_or():
    pass
