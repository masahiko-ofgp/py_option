from __future__ import annotations
from enum import Enum, auto
import typing as t


class OptionType(Enum):
    Some = auto()
    Non = auto()

    def __iter__(self):
        '''HACK:
        Implemented for type annotation of the return value of `Option.new`
        '''
        return self


class Option:
    S: t.TypeAlias = t.Tuple[OptionType, t.Any]
    N: t.TypeAlias = t.Tuple[OptionType,]

    @staticmethod
    def new(value: t.Optional[t.Any] = None) -> t.Union[S, N]:
        ''' Create new Option type.

        Args:
            value: Any type. Default is None.
        Returns:
            If value is None, Returns (OptionType.Non,).
            If value, return (OptionType.Some, value).
        Examples:
            >>> some = Option.new(123)
            >>> some
            (<OptionType.Some: 1>, 123)
            >>> non = Option.new()
            >>> non
            (<OptionType.Non: 2>,)
        '''
        if value is None:
            return (OptionType.Non,)
        else:
            return (OptionType.Some, value)

    @staticmethod
    def is_some(option: t.Union[S, t.Any]) -> bool:
        ''' Returns True if the option is (OptionType.Some, value).

        Args:
            option ((OptionType.Some, value) or else)
        Returns:
            bool
        Examples:
            >>> some = Option.new(123)
            >>> Option.is_some(some)
            True
            >>> non = Option.new()
            >>> Option.is_some(non)
            False
            >>> Option.is_some(123)
            False
        '''
        try:
            ty, value = option
        except:
            return False
        else:
            if ty == OptionType.Some:
                return True
            return False

    @staticmethod
    def is_non(option: t.Union[N, t.Any]) -> bool:
        ''' Returns True if the option is (OptionType.Non,).

        Args:
            option ((OptionType.Non,) or else)
        Returns:
            bool
        Examples:
            >>> non = Option.new()
            >>> Option.is_non(non)
            True
            >>> some = Option.new(123)
            >>> Option.is_non(some)
            False
            >>> Option.is_non(None)
            False
        '''
        try:
            ty, = option
        except:
            return False
        else:
            if ty == OptionType.Non:
                return True
            return False

    @staticmethod
    def expect(option: t.Union[S, t.Any], msg: str) -> t.Union[t.Any, Exception]:
        '''
        If the option is (OptionType.Some, value), return value.
        If the option is (OptionType.Non,) or else, raise TypeError and message.

        Args:
            option ((OptionType.Some, value) or else)
            msg (str)
        Returns:
            value (Any type) or TypeError
        Raises:
            TypeError(msg)
        Examples:
            >>> some = Option.new(123)
            >>> Option.expect(some, "ERROR")
            123
            >>> non = Option.new()
            >>> Option.expect(non, "ERROR")
            Traceback (most recent call last):
                ...
            TypeError: ERROR
            >>> Option.expect(123, "Not Option Type")
            Traceback (most recent call last):
                ...
            TypeError: Not Option Type
        '''
        if Option.is_some(option):
            _, value = option
            return value
        raise TypeError(msg)

    @staticmethod
    def unwrap(option: t.Union[S, t.Any]) -> t.Union[t.Any, Exception]:
        '''
        If the option is (OptionType.Some, value), return value.
        If the option is (OptionType.Non,) or else, raise TypeError.

        Args:
            option ((OptionType.Some, value) or else)
        Returns:
            value (Any type) or TypeError
        Raises:
            TypeError
        Examples:
            >>> some = Option.new(123)
            >>> Option.unwrap(some)
            123
            >>> non = Option.new()
            >>> Option.unwrap(non)
            Traceback (most recent call last):
                ...
            TypeError
            >>> Option.unwrap(123)
            Traceback (most recent call last):
                ...
            TypeError
        '''
        if Option.is_some(option):
            _, value = option
            return value
        raise TypeError

    @staticmethod
    def unwrap_or(option: t.Union[S, t.Any], default: t.Any) -> t.Any:
        '''
        If the option is (OptionType.Some, value), return value.
        If the option is (OptionType.Non,) or else, return default value.

        Args:
            option ((OptionType.Some, value) or else)
            default (Any type)
        Returns:
            value (Any type)
        Examples:
            >>> some = Option.new(123)
            >>> Option.unwrap_or(some, 0)
            123
            >>> non = Option.new()
            >>> Option.unwrap_or(non, 0)
            0
            >>> Option.unwrap_or(123, 0)
            0
        '''
        if Option.is_some(option):
            _, value = option
            return value
        return default

    @staticmethod
    def unwrap_or_else(option: t.Union[S, t.Any], f: t.Callable[..., t.Any]) -> t.Any:
        '''
        If the option is (OptionType.Some, value), return value.
        If the option is (OptionType.Non,) or else, execute f function.

        Args:
            option ((OptionType.Some, value) or else)
            f (function)
        Returns:
            value or the result of f
        Examples:
            >>> some = Option.new(123)
            >>> Option.unwrap_or_else(some, lambda: "Hello")
            123
            >>> non = Option.new()
            >>> Option.unwrap_or_else(non, lambda: "Hello")
            'Hello'
            >>> Option.unwrap_or_else(123, lambda: "Hello")
            'Hello'
        '''
        if Option.is_some(option):
            _, value = option
            return value
        return f()

    @staticmethod
    def map(option: t.Union[S, t.Any],
            f: t.Callable[..., t.Any]) -> t.Union[S, Exception]:
        '''
        If the option is (OptionType.Some, value), f function applies to value and
        return (OptionType.Some, new_value).
        If the option is (OptionType.Non,) or else, raise TypeError.

        Args:
            option ((OptionType.Some, value) or else)
            f (function)
        Returns:
            (OptionType.Some, new_value) or Exception
        Raises:
            TypeError
        Examples:
            >>> some = Option.new(123)
            >>> some
            (<OptionType.Some: 1>, 123)
            >>> some = Option.map(some, lambda x: x + 321)
            >>> some
            (<OptionType.Some: 1>, 444)
            >>> non = Option.new()
            >>> non = Option.map(non, lambda x: x + 321)
            Traceback (most recent call last):
                ...
            TypeError
            >>> Option.map(123, lambda x: x + 321)
            Traceback (most recent call last):
                ...
            TypeError
        '''
        if Option.is_some(option):
            ty, value = option
            if not Option.is_non(value):
                try:
                    new_value = f(value)
                except:
                    raise TypeError
                else:
                    return (ty, new_value)
            else:
                raise TypeError
        else:
            raise TypeError

    @staticmethod
    def map_or(option: t.Union[S, t.Any],
               default: t.Any,
               f: t.Callable[..., t.Any]) -> t.Union[S, t.Any]:
        '''
        If the option is (OptionType.Some, value), f function applies to value and
        return (OptionType.Some, new_value).
        If the option is (OptionType.Non,) or else, return default value.

        Args:
            option ((OptionType.Some, value) or else)
            default (Any type)
            f (function)
        Returns:
            (OptionType.Some, new_value) or default
        Raises:
            TypeError
        Examples:
            >>> some = Option.new(123)
            >>> some
            (<OptionType.Some: 1>, 123)
            >>> some = Option.map_or(some, 0, lambda x: x + 321)
            >>> some
            (<OptionType.Some: 1>, 444)
            >>> non = Option.new()
            >>> non = Option.map_or(non, 0, lambda x: x + 321)
            >>> non
            0
            >>> Option.map_or(123, 0, lambda x: x + 321)
            0
            >>> sn = Option.new(Option.new())
            >>> Option.map_or(sn, 0, lambda x: x + 321)
            0
            >>> some_2 = Option.new(123)
            >>> Option.map_or(some_2, 0, lambda s: s + "Hello")
            Traceback (most recent call last):
                ...
            TypeError
        '''
        if Option.is_some(option):
            ty, value = option
            if not Option.is_non(value):
                try:
                    new_value = f(value)
                except:
                    raise TypeError
                else:
                    return (ty, new_value)
            else:
                return default
        else:
            return default

    @staticmethod
    def map_or_else(option: t.Union[S, t.Any],
                    default_f: t.Callable[..., t.Any],
                    f: t.Callable[..., t.Any]) -> t.Union[S, t.Any]:
        '''
        If the option is (OptionType.Some, value), f function applies to value and
        return (OptionType.Some, new_value).
        If the option is (OptionType.Non,) or else, execute default_f function.

        Args:
            option ((OptionType.Some, value) or else)
            default_f (function)
            f (function)
        Returns:
            (OptionType.Some, new_value) or the result of default_f
        Raises:
            TypeError
        Examples:
            >>> some = Option.new(123)
            >>> some
            (<OptionType.Some: 1>, 123)
            >>> some = Option.map_or_else(some, lambda: 0, lambda x: x + 321)
            >>> some
            (<OptionType.Some: 1>, 444)
            >>> non = Option.new()
            >>> non = Option.map_or_else(non, lambda: 0, lambda x: x + 321)
            >>> non
            0
            >>> Option.map_or_else(123, lambda: 0, lambda x: x + 321)
            0
            >>> sn = Option.new(Option.new())
            >>> Option.map_or_else(sn, lambda: 0, lambda x: x + 321)
            0
            >>> some_2 = Option.new(123)
            >>> Option.map_or_else(some_2, lambda: 0, lambda s: s + "Hello")
            Traceback (most recent call last):
                ...
            TypeError
        '''
        if Option.is_some(option):
            ty, value = option
            if not Option.is_non(value):
                try:
                    new_value = f(value)
                except:
                    raise TypeError
                else:
                    return (ty, new_value)
            else:
                return default_f()
        else:
            return default_f()

    @staticmethod
    def and_option(option: t.Union[S, N],
                   optb: t.Union[S, N]) -> t.Union[t.Union[S, N], Exception]:
        '''
        Returns (OptionType.Non,) if the option is (OptionType.Non,),
        otherwise returns optb.

        Args:
            option ((OptionType.Some, value) or (OptionType.Non,))
            optb ((OptionType.Some, value) or (OptionType.Non,))
        Returns:
            (OptionType.Some, value) or (OptionType.Non,)
        Raises:
            TypeError
        Examples:
            >>> some = Option.new(123)
            >>> some2 = Option.new(456)
            >>> non = Option.new()
            >>> Option.and_option(some, some2)
            (<OptionType.Some: 1>, 456)
            >>> Option.and_option(non, some2)
            (<OptionType.Non: 2>,)
        '''
        if Option.is_non(option):
            return option
        elif Option.is_some(option):
            return optb
        else:
            raise TypeError

    @staticmethod
    def and_then(option: t.Union[S, N],
                 f: t.Callable[..., t.Any]) -> t.Union[t.Union[S, N], Exception]:
        '''
        Returns (OptionType.Non,) if the option is (OptionType.Non,), otherwise
        calls f with the warpped and returns the result.

        Args:
            option ((OptionType.Some, value) or (OptionType.Non,))
            f (function)
        Returns:
            (OptionType.Some, value) or (OptionType.Non,)
        Raises:
            TypeError
        Examples:
            >>> some = Option.new(123)
            >>> non = Option.new()
            >>> Option.and_then(some, lambda x: x + 321)
            (<OptionType.Some: 1>, 444)
            >>> Option.and_then(non, lambda x: x + 321)
            (<OptionType.Non: 2>,)
            >>> Option.and_then(123, lambda x: x + 321)
            Traceback (most recent call last):
                ...
            TypeError
        '''
        if Option.is_some(option):
            return Option.map(option, f)
        elif Option.is_non(option):
            return option
        else:
            raise TypeError

    @staticmethod
    def zip(option: t.Union[S, t.Any],
            optb: t.Union[S, t.Any]) -> t.Union[t.Union[S, N], Exception]:
        '''Zips option with another option.

        Args:
            option ((OptionType.Some, value1) or else)
            optb ((OptionType.Some, value2) or else)
        Returns:
            (OptionType.Some, (value1, value2)) or (OptionType.Non,)
        Raises:
            TypeError
        Examples:
            >>> some1 = Option.new(123)
            >>> some2 = Option.new("Hello")
            >>> Option.zip(some1, some2)
            (<OptionType.Some: 1>, (123, 'Hello'))
            >>> non = Option.new()
            >>> Option.zip(some1, non)
            (<OptionType.Non: 2>,)
            >>> Option.zip(some2, "world")
            Traceback (most recent call last):
                ...
            TypeError
        '''
        if Option.is_non(option):
            return option
        elif Option.is_some(option):
            if Option.is_non(optb):
                return Option.new()
            elif Option.is_some(optb):
                ty, value1 = option
                _, value2 = optb
                return (ty, (value1, value2))
            else:
                raise TypeError
        else:
            raise TypeError

    @staticmethod
    def flatten(option: t.Union[S, t.Any]) -> t.Union[t.Union[S, N], Exception]:
        '''Convert from (Option type, (Option type, value )) to (Option type, value)

        Args:
            option ((OptionType.Some, value) or else)
        Returns:
            (OptionType.Some, value) or (OptionType.Non,)
        Raises:
            TypeError
        Examples:
            >>> sss = Option.new(Option.new(Option.new(123)))
            >>> Option.flatten(sss)
            (<OptionType.Some: 1>, (<OptionType.Some: 1>, 123))
            >>> Option.flatten(Option.flatten(sss))
            (<OptionType.Some: 1>, 123)
            >>> sn = Option.new(Option.new())
            >>> Option.flatten(sn)
            (<OptionType.Non: 2>,)
            >>> n = Option.new()
            >>> Option.flatten(n)
            (<OptionType.Non: 2>,)
            >>> Option.flatten((1,2,3))
            Traceback (most recent call last):
                ...
            TypeError
        '''
        def is_option(op: t.Any) -> bool:
            if Option.is_non(op) or Option.is_some(op):
                return True
            else:
                return False

        if is_option(option):
            if Option.is_non(option):
                return option
            else:
                ty, value = option
                if is_option(value):
                    return value
                else:
                    return option
        else:
           raise TypeError

    @staticmethod
    def filter(option: t.Union[S, t.Any],
               predicate: t.Callable[..., bool]) -> t.Union[t.Union[S, N], Exception]:
        '''
        (OptionType.Some, value) if predicate returns True.
        (OptionType.Non,) if predicate returns False.

        Args:
            option ((OptionType.Some, value) or else)
            predicate (function that return bool)
        Returns:
            (OptionType.Some, value) or (OptionType.Non,)
        Raises:
             TypeError
        Examples:
            >>> some = Option.new(1)
            >>> Option.filter(some, lambda x: x > 0)
            (<OptionType.Some: 1>, 1)
            >>> Option.filter(some, lambda x: x < 0)
            (<OptionType.Non: 2>,)
            >>> non = Option.new()
            >>> Option.filter(non, lambda x: x > 0)
            (<OptionType.Non: 2>,)
            >>> Option.filter(some, lambda x: x + 2)
            Traceback (most recent call last):
                ...
            TypeError
            >>> Option.filter(2, lambda x: x > 0)
            Traceback (most recent call last):
                ...
            TypeError
        '''
        if Option.is_non(option):
            return option
        elif Option.is_some(option):
            _, value = option
            result = predicate(value)
            if result is True:
                return option
            elif result is False:
                return Option.new()
            else:
                raise TypeError
        else:
            raise TypeError

    @staticmethod
    def or_option(option: t.Union[S, t.Any],
                  optb: t.Union[S, t.Any]) -> t.Union[t.Union[S, N], Exception]:
        ''' Returns the option if it is (OptionType.Some, value), otherwise returns optb.

        Args:
            option ((OptionType.Some, value) or else)
            optb   ((OptionType.Some, value) or else)
        Returns:
            (OptionType.Some, value) or (OptionType.Non,)
        Raises:
            TypeError
        Examples:
            >>> x = Option.new(123)
            >>> y = Option.new()
            >>> Option.or_option(x, y)
            (<OptionType.Some: 1>, 123)
            >>> z = Option.new()
            >>> Option.or_option(y, z)
            (<OptionType.Non: 2>,)
            >>> Option.or_option(y, 123)
            Traceback (most recent call last):
                ...
            TypeError
        '''
        if Option.is_some(option):
            return option
        elif Option.is_non(option):
            if Option.is_some(optb):
                return optb
            elif Option.is_non(optb):
                return option
            else:
                raise TypeError
        else:
            raise TypeError
