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
    O: t.TypeAlias = t.Tuple[OptionType, ...]

    @staticmethod
    def new(value: t.Optional[t.Any] = None) -> O:
        ''' Create new Option type.
        If value is None, Returns (OptionType.Non,).
        If value, return (OptionType.Some, value).
        '''
        if value is None:
            return (OptionType.Non,)
        else:
            return (OptionType.Some, value)

    @staticmethod
    def is_some(option: OptionType) -> bool:
        ''' Returns True if the option is (OptionType.Some, value). '''
        try:
            ty, value = option
        except:
            return False
        else:
            if ty == OptionType.Some:
                return True
            return False

    @staticmethod
    def is_non(option: OptionType) -> bool:
        ''' Returns True if the option is (OptionType.Non,). '''
        try:
            ty, = option
        except:
            return False
        else:
            if ty == OptionType.Non:
                return True
            return False

    @staticmethod
    def expect(option: OptionType, msg: str) -> t.Union[t.Any, Exception]:
        '''
        If the option is (OptionType.Some, value), return value.
        If the option is (OptionType.Non,) or else, raise TypeError and message.
        '''
        if Option.is_some(option):
            _, value = option
            return value
        raise TypeError(msg)

    @staticmethod
    def unwrap(option: OptionType) -> t.Union[t.Any, Exception]:
        '''
        If the option is (OptionType.Some, value), return value.
        If the option is (OptionType.Non,) or else, raise TypeError.
        '''
        if Option.is_some(option):
            _, value = option
            return value
        raise TypeError

    @staticmethod
    def unwrap_or(option: OptionType, default: t.Any) -> t.Any:
        '''
        If the option is (OptionType.Some, value), return value.
        If the option is (OptionType.Non,) or else, return default value.
        '''
        if Option.is_some(option):
            _, value = option
            return value
        return default

    @staticmethod
    def unwrap_or_else(option: OptionType, f: t.Callable[..., t.Any]) -> t.Any:
        '''
        If the option is (OptionType.Some, value), return value.
        If the option is (OptionType.Non,) or else, execute f function.
        '''
        if Option.is_some(option):
            _, value = option
            return value
        return f()

    @staticmethod
    def map(option: OptionType, f: t.Callable[..., t.Any]) -> t.Union[O, Exception]:
        '''
        If the option is (OptionType.Some, value), f function applies to value and
        return (OptionType.Some, new_value).
        If the option is (OptionType.Non,) or else, raise TypeError.
        '''
        if Option.is_some(option):
            _, value = option
            if not Option.is_non(value):
                new_value = f(value)
                return Option.new(new_value)
            else:
                raise TypeError
        else:
            raise TypeError

    @staticmethod
    def map_or(option: OptionType,
               default: t.Any,
               f: t.Callable[..., t.Any]) -> t.Union[O, t.Any]:
        '''
        If the option is (OptionType.Some, value), f function applies to value and
        return (OptionType.Some, new_value).
        If the option is (OptionType.Non,) or else, return default value.
        '''
        if Option.is_some(option):
            _, value = option
            if not Option.is_non(value):
                new_value = f(value)
                return Option.new(new_value)
            else:
                return default
        else:
            return default

    @staticmethod
    def map_or_else(option: OptionType,
                    default_f: t.Callable[..., t.Any],
                    f: t.Callable[..., t.Any]) -> t.Union[O, t.Any]:
        '''
        If the option is (OptionType.Some, value), f function applies to value and
        return (OptionType.Some, new_value).
        If the option is (OptionType.Non,) or else, execute default_f function.
        '''
        if Option.is_some(option):
            _, value = option
            if not Option.is_non(value):
                new_value = f(value)
                return Option.new(new_value)
            else:
                return default_f()
        else:
            return default_f()
