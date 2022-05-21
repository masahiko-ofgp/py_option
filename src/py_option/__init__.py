import typing as t


class Some:
    def __init__(self, value: t.Any) -> None:
        self.value = value

    def __eq__(self, rhs):
        # type: (t.Union[Some, t.Any]) -> bool
        if not isinstance(rhs, Some):
            return NotImplemented
        return self.value == rhs.value

    def __ne__(self, rhs):
        # type: (t.Union[Some, t.Any]) -> bool
        if not isinstance(rhs, Some):
            return NotImplemented
        return self.value != rhs.value
    
    def __repr__(self) -> str:
        return f"Some({self.value})"

    
class Non:
    def __init__(self) -> None:
        self.value = None

    def __eq__(self, rhs):
        # type: (t.Union[Non, t.Any]) -> bool
        if not isinstance(rhs, Non):
            return False
        return True

    def __ne__(self, rhs):
        # type: (t.Union[Non, t.Any]) -> bool
        if not isinstance(rhs, Non):
            return True
        return False
    
    def __repr__(self) -> str:
        return "None"


class Option:
    @staticmethod
    def is_some(option: t.Union[Some, Non]) -> bool:
        return isinstance(option, Some)

    @staticmethod
    def is_non(option: t.Union[Some, Non]) -> bool:
        return isinstance(option, Non)

    @staticmethod
    def expect(option: t.Union[Some, Non], msg: str) -> t.Union[t.Any, Exception]:
        if Option.is_some(option):
            return option.value
        raise ValueError(msg)

    @staticmethod
    def unwrap(option: t.Union[Some, Non]) -> t.Union[t.Any, Exception]:
        if Option.is_some(option):
            return option.value
        raise ValueError

    @staticmethod
    def unwrap_or(option: t.Union[Some, Non], default: t.Any) -> t.Any:
        if Option.is_some(option):
            return option.value
        return default

    @staticmethod
    def unwrap_or_else(option: t.Union[Some, Non], f: t.Callable[..., t.Any]) -> t.Any:
        if Option.is_some(option):
            return option.value
        return f()

    @staticmethod
    def map(option: t.Union[Some, Non], f: t.Callable[..., t.Any]) -> t.Union[Some, Exception]:
        if Option.is_some(option):
            try:
                some = Some(f(option.value))
            except:
                raise ValueError
            else:
                return some
        raise ValueError("Not Some")

    @staticmethod
    def map_or(option: t.Union[Some, Non],
               default: t.Any,
               f: t.Callable[..., t.Any]) -> t.Union[Some, t.Any]:
        if Option.is_some(option):
           try:
               some = Some(f(option.value))
           except:
               raise ValueError
           else:
               return some
        return default

    @staticmethod
    def map_or_else(option: t.Union[Some, Non],
                    default_f: t.Callable[..., t.Any],
                    f: t.Callable[..., t.Any]) -> t.Union[Some, t.Any]:
        if Option.is_some(option):
            try:
                some = Some(f(option.value))
            except:
                raise ValueError
            else:
                return some
        return default_f()
