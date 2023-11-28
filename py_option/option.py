from abc import abstractmethod, ABC


class OptionTypeError(Exception):
    """
    """
    def __init__(self, msg):
        self.msg = msg


class OptionType(ABC):
    """Interface of Option.
    """
    @abstractmethod
    def is_some(self): pass

    @abstractmethod
    def is_non(self): pass

    @abstractmethod
    def unwrap(self): pass

    @abstractmethod
    def unwrap_or(self, default): pass


class Some(OptionType):
    """
    """
    def __init__(self, val):
        self.val = val

    def is_some(self):
        return True

    def is_non(self):
        return False

    def unwrap(self):
        return self.val

    def unwrap_or(self, default):
        del(default)
        return self.val

    def __repr__(self):
        return f"Option::Some({self.val})"


class Non(OptionType):
    """
    """
    def __init__(self):
        self.val = None

    def is_some(self):
        return False

    def is_non(self):
        return True

    def unwrap(self):
        raise OptionTypeError("Option::Non type does not have val.")

    def unwrap_or(self, default):
        return default

    def __repr__(self):
        return "Option::Non"

class Option(OptionType):
    """
    """
    def __init__(self, val=None):
        if val is None:
            self.typ = Non()
        else:
            self.typ = Some(val)

    def is_some(self):
        return self.typ.is_some()

    def is_non(self):
        return self.typ.is_non()

    def unwrap(self):
        return self.typ.unwrap()

    def unwrap_or(self, default):
        return self.typ.unwrap_or(default)

    def __repr__(self):
        return f"{self.typ}"
