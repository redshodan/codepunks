from codepunks.nested import NestedDict, NestedList


def testDictEquality():
    d = {"s1": {"k1": "v1"}, "s2": {"k2": "v2"}}

    c = NestedDict()
    c.dict("s1")
    c["s1"]["k1"] = "v1"
    c.dict("s2")
    c["s2"]["k2"] = "v2"

    assert d == c


def testMissingException():
    c = NestedDict()
    c["s1"] = "v1"

    assert c["s1"] == "v1"
    try:
        c["s2"] is None
    except KeyError:
        pass
    else:
        assert False


def testMissingNone():
    c = NestedDict(notfound=None)
    c["s1"] = "v1"
    assert c["s1"] == "v1"
    assert c["s2"] is None


def testDictBuild():
    c = NestedDict()
    d3 = c.dict("d1").dict("d2").dict("d3")
    assert c["d1"]["d2"]["d3"] is d3


def testRoot():
    c = NestedDict()
    d1 = c.dict("d1")
    d2 = d1.dict("d2")
    d3 = d2.dict("d3")
    assert d1.root() is c
    assert d2.root() is c
    assert d3.root() is c


def testParent():
    c = NestedDict()
    d1 = c.dict("d1")
    d2 = d1.dict("d2")
    d3 = d2.dict("d3")
    assert d3.parent is d2
    assert d2.parent is d1
    assert d1.parent is c


def testList():
    c = NestedDict()
    l1 = c.list("l1")
    ld1 = l1.dict()
    d2 = ld1.dict("d2")
    l2 = d2.list("l2")
    assert c["l1"][0]["d2"]["l2"] is l2


def testListMissingException():
    c = NestedDict()
    l1 = c.list("l1")
    l1.dict()

    try:
        c["l1"][1]
    except IndexError:
        pass
    else:
        assert False


def testListMissingNone():
    c = NestedDict(notfound=None)
    l1 = c.list("l1")
    l1.dict()
    assert c["l1"][1] is None


def testFind():
    c = NestedDict()
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
    c = NestedDict()
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


def testRationalize():
    c = NestedDict()
    d1 = c.dict("d1")
    d2 = d1["d2"] = {}
    k2 = d2["k2"] = "v2"
    l2 = d1["l2"] = []
    k3 = l2.append("k3")
    c2 = c.copy()
    c.rationalize()

    assert isinstance(d1["d2"], NestedDict)
    assert isinstance(d1["l2"], NestedList)
    assert c == c2


def testAutoRationalizeDict():
    c = NestedDict()
    d1 = c.dict("d1")
    d2 = d1["d2"] = {}
    k2 = d2["k2"] = "v2"
    l2 = d1["l2"] = []
    k3 = l2.append("k3")
    c2 = c.copy()

    assert isinstance(d1["d2"], dict)
    assert isinstance(d1["l2"], list)

    assert c["d1/d2/k2"] is k2

    assert isinstance(d1["d2"], NestedDict)
    assert isinstance(d1["l2"], NestedList)
    assert c == c2


def testAutoRationalizeList():
    c = NestedDict()
    l1 = c.list("l1")
    d2 = l1.append({})
    k2 = d2["k2"] = "v2"
    l2 = l1.append([])
    k3 = "k3"
    l2.append(k3)
    c2 = c.copy()

    assert isinstance(l1[0], dict)
    assert isinstance(l1[1], list)

    assert c["l1/1/0"] is k3

    assert isinstance(l1[0], NestedDict)
    assert isinstance(l1[1], NestedList)
    assert c == c2


def testCopyList():
    d = ["s1", {"k1": "v1"}, {"s2": {"k2": ["v2", "v3"]}}]
    c = NestedList(d)

    assert d == c
    assert isinstance(c["1"], NestedDict)
    assert isinstance(c[1], NestedDict)
    assert isinstance(c["2/s2"], NestedDict)
    assert isinstance(c["2/s2/k2"], NestedList)


def testCopyDict():
    d = {"s1": ["v0", "v0.1", "v0.2"],
         "k1": "v1",
         "s2": {"k2": ["v2", "v3"]}}
    c = NestedDict(d)

    assert d == c
    assert isinstance(c["s1"], NestedList)
    assert isinstance(c["s2"], NestedDict)
    assert isinstance(c["s2/k2"], NestedList)


def testMergeEmptyDict():
    d = {"s1": {"s2": {"k3": "v3"}}}
    c = NestedDict()
    c.merge(d)

    assert isinstance(c["s1"], NestedDict)
    assert isinstance(c["s1/s2"], NestedDict)
    assert isinstance(c["s1/s2/k3"], str)


def testMergeEmptyList():
    d = [[["k3", "v3"]]]
    c = NestedList()
    c.merge(d)

    assert isinstance(c["0"], NestedList)
    assert isinstance(c["0/0"], NestedList)
    assert isinstance(c["0/0/0"], str)
    assert isinstance(c["0/0/1"], str)


def testMergeDict():
    d = {"s1": {"s2": {"k3": "v3"}, "s2a": {"k3a": "v3a"}}}
    c = NestedDict()
    s1 = c.dict("s1")
    k1 = s1["k1"] = "v1"
    s2 = s1.dict("s2")
    k2 = s2["k2"] = "v2"
    c.merge(d)

    assert isinstance(c["s1"], NestedDict)
    assert isinstance(c["s1/s2"], NestedDict)
    assert isinstance(c["s1/s2/k3"], str)


def testMergeList():
    d = [[["k3", "v3"]]]
    c = NestedList()
    c.merge(d)

    assert isinstance(c["0"], NestedList)
    assert isinstance(c["0/0"], NestedList)
    assert isinstance(c["0/0/0"], str)
    assert isinstance(c["0/0/1"], str)
