import os
import configparser
import json


class Config(dict):
    SRC_INI = object()
    SRC_JSON = object()
    SRC_YAML = object()
    SRC_DB = object()
    SRC_CLI = object()
    DEF_SRCS = [SRC_INI, SRC_JSON, SRC_YAML, SRC_DB, SRC_CLI]


    def __init__(self, sources=DEF_SRCS):
        self.substs = dict()
        self.sources = sources
        self.setSubsts()


    def setSubsts(self):
        # %(install)s
        install = "/".join(os.path.dirname(__file__).split("/")[:-1])
        self.substs["install"] = install
        
        # # %(here)s
        # here = os.path.dirname(os.path.abspath(self.filename))
        # self.substs["here"] = here


    def get(self, key):
        if val and "%(here)s" in val:
            return val.replace("%(here)s",
                               super().get(configparser.DEFAULTSECT, "here"))
        elif val and "%(install)s" in val:
            return val.replace("%(install)s",
                               super().get(configparser.DEFAULTSECT, "install"))
        else:
            return val


    def print(self):
        print(json.dumps(self, sort_keys=True, indent=4))

