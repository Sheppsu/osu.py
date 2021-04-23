def check_scope(func):
    def check(self, other):
        if not isinstance(other, self.__class__) and type(other) != str:
            raise TypeError(f"Cannot compare type Scope with type {type(other).__name__}")
        if isinstance(other, self.__class__):
            other = other.scope
        if other not in self.valid_scopes:
            raise NameError(f"{other} is not a valid scope.")
        return func(self, other)
    return check