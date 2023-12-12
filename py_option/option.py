from abc import abstractmethod, ABC


class OptionTypeError(Exception):
    def __init__(self, msg):
        self.msg = msg


class OptionType(ABC):
    """Interface of OptionType.
    
    """
    @abstractmethod
    def is_some(self): pass

    @abstractmethod
    def is_some_and(self, f): pass

    @abstractmethod
    def is_non(self): pass

    @abstractmethod
    def expect(self, msg): pass

    @abstractmethod
    def filter(self, predicate): pass

    @abstractmethod
    def unwrap(self): pass

    @abstractmethod
    def unwrap_or(self, default): pass

    @abstractmethod
    def __repr__(self): pass

    @abstractmethod
    def __eq__(self, rhs): pass


class Some(OptionType):
    """Some is OptionType with some value.
    
    """
    def __init__(self, val):
        self.val = val

    def is_some(self):
        return True

    def is_some_and(self, f):
        return (self.is_some and f(self.val))

    def is_non(self):
        return False

    def expect(self, msg):
        return self.val

    def filter(self, predicate):
        if predicate(self.val):
            return self
        else:
            return Option.new()

    def unwrap(self):
        return self.val

    def unwrap_or(self, default):
        del(default)
        return self.val

    def __repr__(self):
        return f"Option::Some({self.val})"

    def __eq__(self, rhs):
        if rhs.is_some():
            return self.val == rhs.val
        else:
            return False


class Non(OptionType):
    """Non is OptionType with no value.
    
    """
    def __init__(self):
        self.val = None

    def is_some(self):
        return False
    
    def is_some_and(self, f):
        return False

    def is_non(self):
        return True

    def expect(self, msg):
        return msg

    def filter(self, predicate):
        return self

    def unwrap(self):
        raise OptionTypeError("Option::Non type does not have val.")

    def unwrap_or(self, default):
        return default

    def __repr__(self):
        return "Option::Non"

    def __eq__(self, rhs):
        return rhs.is_non()


class Option():
    """Option class create Some or Non.

    """
    @staticmethod
    def new(val=None):
        """Create new Some(x) or Non.

        If val is not None, return Some(val).
        """
        if val is None:
            return Non()
        else:
            return Some(val)
