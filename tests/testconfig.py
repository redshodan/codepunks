from codepunks.config import Config


def testDictEquality():
    d = {"s1": {"k1": "v1"}, "s2": {"k2": "v2"}}

    c = Config()
    c.dict("s1")
    c["s1"]["k1"] = "v1"
    c.dict("s2")
    c["s2"]["k2"] = "v2"

    assert d == c


def testMissingException():
    c = Config()
    c["s1"] = "v1"

    assert c["s1"] == "v1"
    try:
        c["s2"] is None
    except KeyError:
        pass
    else:
        assert False


def testMissingNone():
    c = Config(notfound=None)
    c["s1"] = "v1"
    assert c["s1"] == "v1"
    assert c["s2"] is None


def testDictBuild():
    c = Config()
    d3 = c.dict("d1").dict("d2").dict("d3")
    assert c["d1"]["d2"]["d3"] is d3


def testRoot():
    c = Config()
    d1 = c.dict("d1")
    d2 = d1.dict("d2")
    d3 = d2.dict("d3")
    assert d1.root() is c
    assert d2.root() is c
    assert d3.root() is c


def testParent():
    c = Config()
    d1 = c.dict("d1")
    d2 = d1.dict("d2")
    d3 = d2.dict("d3")
    assert d3.parent is d2
    assert d2.parent is d1
    assert d1.parent is c


def testList():
    c = Config()
    l1 = c.list("l1")
    ld1 = l1.dict()
    d2 = ld1.dict("d2")
    l2 = d2.list("l2")
    assert c["l1"][0]["d2"]["l2"] is l2


def testListMissingException():
    c = Config()
    l1 = c.list("l1")
    l1.dict()

    try:
        c["l1"][1]
    except IndexError:
        pass
    else:
        assert False


def testListMissingNone():
    c = Config(notfound=None)
    l1 = c.list("l1")
    l1.dict()
    assert c["l1"][1] is None


def testFind():
    c = Config()
    d1 = c.dict("d1")
    k1 = d1["k1"] = "v1"
    d2 = d1.dict("d2")
    k2 = d2["k2"] = "v2"
    d3 = d2.dict("d3")
    k3 = d3["k3"] = "v3"

    assert c["d1"] is d1
    assert c["d1/k1"] is k1
    assert c["d1/k1"] == "v1"
    assert c["d1/d2"] is d2
    assert c["d1/d2/k2"] is k2
    assert c["d1/d2/k2"] == "v2"
    assert c["d1/d2/d3"] is d3
    assert c["d1/d2/d3/k3"] is k3
    assert c["d1/d2/d3/k3"] == "v3"


def testFindList():
    c = Config()
    d1 = c.dict("d1")
    k1 = d1["k1"] = "v1"
    d2 = d1.dict("d2")
    k2 = d2["k2"] = "v2"
    l3 = d2.list("l3")
    k3 = l3.append("v3")
    d4 = l3.dict()
    k4 = d4["k4"] = "v4"
    assert c["d1"] is d1
    assert c["d1/k1"] is k1
    assert c["d1/k1"] == "v1"
    assert c["d1/d2"] is d2
    assert c["d1/d2/k2"] is k2
    assert c["d1/d2/k2"] == "v2"
    assert c["d1/d2/l3"] is l3
    assert c["d1/d2/l3/0"] is k3
    assert c["d1/d2/l3/0"] == "v3"
    assert c["d1/d2/l3/1"] is d4
    assert c["d1/d2/l3/1/k4"] is k4
    assert c["d1/d2/l3/1/k4"] == "v4"
