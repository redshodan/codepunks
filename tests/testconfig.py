import argparse
import configparser
from codepunks.config import (Config, INISource, XMLSource, JSONSource,
                              YAMLSource, ArgParserSource)


ARGS1 = argparse.Namespace()
ARGS1.apkey1 = "apval1"
ARGS1.apkey2 = "apval2"
ARGS1.apkey3 = "apval3"


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


def testArgParserSource():
    c = Config(ArgParserSource(ARGS1))
    c.load()


def testAllSources():
    c = Config([INISource("tests/config/config.ini"),
                XMLSource("tests/config/config.xml"),
                JSONSource("tests/config/config.json"),
                YAMLSource("tests/config/config.yml"),
                ArgParserSource(ARGS1)])
    c.load()
