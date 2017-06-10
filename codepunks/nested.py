import json


KEY_ERR = KeyError()


"""
d = NestedDict()
d["1"]["2"]["3"].setDefault("foo", "bar")
d.setDefault("1/2/3/foo", "bar")

"""


class BaseNested():
    def __init__(self, parent=None, notfound=KEY_ERR, path_delim="/"):
        self.parent = parent
        self.notfound = notfound
        self.path_delim = path_delim


    def __str__(self):
        return json.dumps(self, sort_keys=True, indent=4)


    def root(self):
        if self.parent:
            return self.parent.root()
        else:
            return self


class NestedList(BaseNested, list):
    def dict(self):
        nd = NestedDict(parent=self, notfound=self.notfound)
        self.append(nd)
        return nd


    def list(self):
        nl = NestedList(parent=self, notfound=self.notfound)
        self.append(nl)
        return nl


    def append(self, item):
        super().append(item)
        return item


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
                return item.__getitem__(path[1:])
        except IndexError as e:
            if isinstance(self.notfound, KeyError):
                raise e
            else:
                return None


class NestedDict(BaseNested, dict):
    def __missing__(self, key):
        if isinstance(self.notfound, KeyError):
            raise KeyError(key)
        else:
            return None


    def dict(self, key):
        self[key] = NestedDict(parent=self, notfound=self.notfound)
        return self[key]


    def list(self, key):
        self[key] = NestedList(parent=self, notfound=self.notfound)
        return self[key]


    def __getitem__(self, key):
        if isinstance(key, list):
            path = key
        else:
            path = key.split(self.path_delim)
        if len(path) == 1:
            return super().__getitem__(path[0])
        else:
            item = super().__getitem__(path[0])
            return item.__getitem__(path[1:])
