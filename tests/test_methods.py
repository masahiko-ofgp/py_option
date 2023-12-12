from py_option import Option


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
    assert s.is_some_and(lambda x: x + 321) == 444
