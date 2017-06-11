import json


KEY_ERR = KeyError()


class BaseNested():
    def __init__(self, parent=None, notfound=KEY_ERR, path_delim="/"):
        self.parent = parent
        self.notfound = notfound
        self.path_delim = path_delim


    def __str__(self):
        return json.dumps(self, sort_keys=True, indent=4)


    def dict(self, key=None):
        nd = NestedDict(parent=self, notfound=self.notfound)
        self.__store__(key, nd)
        return nd


    def list(self, key=None):
        nl = NestedList(parent=self, notfound=self.notfound)
        self.__store__(key, nl)
        return nl


    def root(self):
        if self.parent:
            return self.parent.root()
        else:
            return self


    def rationalize(self):
        for key, val in self.iterate():
            if isinstance(val, (NestedDict, NestedList)):
                val.rationalize()
            elif isinstance(val, list):
                nl = NestedList(parent=self, notfound=self.notfound)
                nl.extend(val)
                self.__store__(key, nl)
                nl.rationalize()
            elif isinstance(val, dict):
                nd = NestedDict(parent=self, notfound=self.notfound)
                nd.update(val)
                self.__store__(key, nd)
                nd.rationalize()


    def merge(self, data):
        pass


class NestedList(BaseNested, list):
    def __init__(self, data=None, **kwargs):
        super().__init__(**kwargs)
        if isinstance(data, list):
            self.extend(data)
            self.rationalize()
        elif data is not None:
            raise TypeError("Wrong type " + str(type(data)))


    def __store__(self, key, value):
        if key is not None:
            self[key] = value
        else:
            self.append(value)


    def append(self, item):
        super().append(item)
        return item


    def iterate(self):
        return enumerate(self)


    def __getitem__(self, key):
        try:
            if isinstance(key, list):
                path = key
            elif isinstance(key, str):
                path = key.split(self.path_delim)
            else:
                path = [key]
            key = int(path[0])
            if len(path) == 1:
                return super().__getitem__(key)
            else:
                item = super().__getitem__(key)
                if isinstance(item, (NestedDict, NestedList)):
                    return item.__getitem__(path[1:])
                elif isinstance(item, (list, dict)):
                    self.rationalize()
                item = super().__getitem__(key)
                return item.__getitem__(path[1:])
        except IndexError as e:
            if isinstance(self.notfound, KeyError):
                raise e
            else:
                return None


class NestedDict(BaseNested, dict):
    def __init__(self, data=None, **kwargs):
        super().__init__(**kwargs)
        if isinstance(data, dict):
            self.update(data)
            self.rationalize()
        elif data is not None:
            raise TypeError("Wrong type " + str(type(data)))


    def __missing__(self, key):
        if isinstance(self.notfound, KeyError):
            raise KeyError(key)
        else:
            return None


    def __store__(self, key, value):
        self[key] = value


    def iterate(self):
        return self.items()


    def __getitem__(self, key):
        if isinstance(key, list):
            path = key
        else:
            path = key.split(self.path_delim)
        if len(path) == 1:
            return super().__getitem__(path[0])
        else:
            item = super().__getitem__(path[0])
            if isinstance(item, (NestedDict, NestedList)):
                return item.__getitem__(path[1:])
            elif isinstance(item, (list, dict)):
                self.rationalize()
            item = super().__getitem__(path[0])
            return item.__getitem__(path[1:])
