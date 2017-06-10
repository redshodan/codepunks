import pytest

from codepunks.config import Config


def testBasic():
    c = Config()
    c["s1"] = {}
    c["s1"]["k1"] = "v1"
    c["s2"] = {}
    c["s2"]["k2"] = "v2"

    c.print()
