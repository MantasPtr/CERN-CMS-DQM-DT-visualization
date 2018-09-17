class ImmutableDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__hash = None

    __delitem__ = None
    __setitem__ = None
    pop = None
    popitem = None
    setdefault = None
    update = None
    
    def __hash__(self):
        if self.__hash is None:
            self._hash = 0
            for key, value in self.items():
                self._hash ^= hash(key)
                self._hash ^= hash(value)             
        return self._hash

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))
