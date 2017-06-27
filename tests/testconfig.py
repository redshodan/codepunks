import configparser
from codepunks.config import Config, INISource, XMLSource, JSONSource, YAMLSource


def testEmptyCfg():
    Config()


def testINISource():
    c = Config(INISource("tests/config/config.ini"))
    c.load()


def testINISourcePreBuilt():
    fname = "tests/config/config.ini"
    parser = configparser.ConfigParser()
    parser.read(fname)
    c = Config(INISource(fname, cfgparser=parser))
    c.load()


def testINISource2():
    c = Config([INISource("tests/config/config.ini"),
                INISource("tests/config/config2.ini")])
    c.load()


def testXMLSource():
    c = Config(XMLSource("tests/config/config.xml"))
    c.load()


def testJSONSource():
    c = Config(JSONSource("tests/config/config.json"))
    c.load()


def testYAMLSource():
    c = Config(YAMLSource("tests/config/config.yml"))
    c.load()


def testAllSources():
    c = Config([INISource("tests/config/config.ini"),
                XMLSource("tests/config/config.xml"),
                JSONSource("tests/config/config.json"),
                YAMLSource("tests/config/config.yml")])
    c.load()
