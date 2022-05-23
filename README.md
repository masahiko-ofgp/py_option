# Py_Option

This library is something like Rust's `Option`.

Of course, it's not as convenient as Rust. However, there may be
useful situations for pattern matching introduced in Python 3.10.


## Environment

- Python 3.10
- poetry
- mypy
- pytest


## Usage

```
>>> import py_option as option
>>> some = option.Option.new(123)
>>> some
(<OptionType.Some: 1>, 123)
>>> non = option.Option.new()
>>> non
(<OptionType.Non: 2>,)
>>> some = option.Option.map(some, lambda x: x + 321)
>>> some
(<OptionType.Some: 1>, 444)
```