import os
import configparser
import json


from .nested import KEY_ERR, NestedDict


class Config(NestedDict):
    INI = object()
    XML = object()
    JSON = object()
    YAML = object()
    DB = object()
    CLI = object()


    def __init__(self, sources=[], notfound=KEY_ERR, defaults={}):
        super().__init__(notfound=notfound)
        self.substs = dict()
        self.sources = sources
        self.defaults = defaults
        self._setupSubsts()


    def addSubst(self, key, val):
        self.substs[key] = val


    def delSubst(self, key):
        del self.substs[key]


    def _setupSubsts(self):
        # %(install)s
        install = "/".join(os.path.dirname(__file__).split("/")[:-1])
        self.substs["install"] = install

        # # %(here)s
        # here = os.path.dirname(os.path.abspath(self.filename))
        # self.substs["here"] = here


    # def get(self, key):
    #     if val and "%(here)s" in val:
    #         return val.replace("%(here)s",
    #                            super().get(configparser.DEFAULTSECT, "here"))
    #     elif val and "%(install)s" in val:
    #         return val.replace("%(install)s",
    #                            super().get(configparser.DEFAULTSECT, "install"))
    #     else:
    #         return val
