from py_option import OptionTypeError, Some, Non
import pytest


s = Some(123)
n = Non()

ss = Some(s)
sn = Some(n)


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

    assert ss.expect("Panic!!") == Some(123)
    assert sn.expect("Panic!!") == Non


def test_filter():
    assert s.filter(lambda x: x % 2 == 0) == Non
    assert s.filter(lambda x: x % 2 == 1) == Some(123)
    assert n.filter(lambda x: x % 2 == 0) == Non

    with pytest.raises(TypeError):
        ss.filter(lambda x: x % 2 == 0)

    with pytest.raises(TypeError):
        sn.filter(lambda x: x % 2 == 0)


def test_unwrap():
    assert s.unwrap() == 123

    with pytest.raises(OptionTypeError):
        n.unwrap()

    assert ss.unwrap() == Some(123)
    assert sn.unwrap() == Non


def test_unwrap_or():
    assert s.unwrap_or("Default") == 123
    assert n.unwrap_or("Default") == "Default"
    assert ss.unwrap_or("Default") == Some(123)
    assert sn.unwrap_or("Default") == Non


def test_and():
    assert s.and_(n) == Non
    assert n.and_(s) == Non
    assert n.and_(n) == Non
    assert s.and_(ss) == Some(Some(123))
    assert s.and_(sn) == Some(Non)
    assert ss.and_(sn) == Some(Non)


def test_or():
    assert s.or_(n) == Some(123)
    assert n.or_(s) == Some(123)
    assert s.or_(ss) == Some(123)
    assert ss.or_(sn) == Some(Some(123))


def test_and_then():
    assert s.and_then(str) == Some("123")
