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
        If value is None, Returns (OptionType.Non,).
        If value, return (OptionType.Some, value).
        '''
        if value is None:
            return (OptionType.Non,)
        else:
            return (OptionType.Some, value)

    @staticmethod
    def is_some(option: t.Union[S, t.Any]) -> bool:
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
    def is_non(option: t.Union[N, t.Any]) -> bool:
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
    def expect(option: t.Union[S, t.Any], msg: str) -> t.Union[t.Any, Exception]:
        '''
        If the option is (OptionType.Some, value), return value.
        If the option is (OptionType.Non,) or else, raise TypeError and message.
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
        '''
        if Option.is_some(option):
            return Option.map(option, f)
        elif Option.is_non(option):
            return option
        else:
            raise TypeError