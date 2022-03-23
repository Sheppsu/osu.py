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


def create_autoclass_for_sphinx():
    with open('objects.py', 'r') as f:
        info = f.readline()
        while info:
            if info.startswith('class'):
                name = info.split()[1]
                if '(' in name:
                    name = name.split('(')[0]
                else:
                    name = name[:-1]
                content = f"{name}\n{'^' * len(name)}\n.. autoclass:: osu.{name}\n   :members:\n\n"
                with open('text.txt', 'a') as f2:
                    f2.write(content)
                    f2.close()
            info = f.readline()
        f.close()


def get_item_else(data, key, default):
    return data[key] if key in data else default
