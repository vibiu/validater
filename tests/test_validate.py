# coding:utf-8

from datetime import datetime
from validater import validate, add_validater
from dateutil import parser


def test_1():

    s1 = {
        "desc": "desc of the key",
        "required": True,
        "validate": "int",
        "default": "321",
    }
    obj1 = "sda"
    (error, value) = validate(obj1, s1)
    assert error
    assert value is None


def test_2():

    s2 = [{
        "desc": "desc of the key",
        "required": True,
        "validate": "int",
        "default": "321",
    }]
    obj2 = ["sda", 1, 2, 3]

    (error, value) = validate(obj2, s2)
    assert error[0][0] == "[0]"
    assert "desc of the key" in error[0][1]
    assert value == [None, 1, 2, 3]


def test_6():
    s6 = [{
        "key1": {
            "desc": "desc of the key",
            "required": True,
            "validate": "int",
            "default": "321",
        }
    }]
    obj6 = [{
        "key1": "123"
    }, {
        "key": "123"
    }, {
        "key1": "asd"
    }, {
        "kkk": "1234"
    }]

    (error, value) = validate(obj6, s6)
    assert len(error) == 1
    assert error[0][0] == "[2].key1"
    assert value == [{"key1": 123}, {"key1": 321},
                     {"key1": None}, {"key1": 321}, ]


def test_3():
    schema3 = {
        "key1": {
            "desc": "desc of the key",
            "required": True,
            "validate": "int",
            "default": "321",
        },
        "key2": {
            "desc": "desc of the key",
            "required": True,
            "validate": "str",
        },
        "key3": {
            "desc": "desc of the key",
            "required": True,
            "validate": "datetime",
            "default": "",
        }
    }
    obj3 = {
        "key1": "123",
        "key2": u"haha",
        "key3": "2015-09-01 14:42:35"
    }

    (error, value) = validate(obj3, schema3)
    assert len(error) == 1
    assert error[0][0] == "key2"
    assert "desc of the key" in error[0][1]
    assert value == {
        "key1": 123,
        "key2": None,
        "key3": parser.parse("2015-09-01 14:42:35")
    }


def test_4():
    schema4 = {
        "key1": [{
            "desc": "desc of the key",
            "required": True,
            "validate": "int",
            "default": "321",
        }]
    }
    obj4 = {
        "key1": ["123", "32", "asd"]
    }
    (error, value) = validate(obj4, schema4)
    assert len(error) == 1
    assert error[0][0] == "key1.[2]"
    assert "desc of the key" in error[0][1]
    assert value == {
        "key1": [123, 32, None]
    }


def test_5():
    schema5 = {
        "key1": {
            "desc": "desc of the key",
            "required": True,
            "validate": "int",
            "default": "321",
        },
        "key2": [{
            "desc": "desc of the key",
            "required": True,
            "validate": "int",
        }],
        "key3": {
            "key1": {
                "desc": "desc of the key",
                "required": True,
                "validate": "int",
            },
            "key2": [{
                "desc": "desc of the key",
                "required": True,
                "validate": "int",
            }],
            "key3": {
                "desc": "desc of the key",
                "required": True,
                "validate": "int",
            },
            "key4": {
                "desc": "desc of the key",
                "validate": "int",
            },
        }
    }
    obj5 = {
        "key1": "123",
        "key2": ["123", "32", "asd"],
        "key3": {
            "key1": "123",
            "key2": ["123", "32", "asd"],
        }
    }

    (error, value) = validate(obj5, schema5)
    assert len(error) == 3
    error = dict(error)
    assert "int" in error["key2.[2]"]
    assert "int" in error["key3.key2.[2]"]
    assert "required" in error["key3.key3"]
    assert value == {
        "key1": 123,
        "key2": [123, 32, None],
        "key3": {
            "key1": 123,
            "key2": [123, 32, None],
            "key3": None,
            "key4": None
        }
    }


def test_addvalidater():
    def plus_int(v):
        try:
            return (int(v) > 0, int(v))
        except:
            return (False, None)
    add_validater("+int", plus_int)

    s = {
        "key": [{
            "desc": "+int",
            "required": True,
            "validate": "+int"
        }]
    }
    obj = {"key": ["123", "0", "-123"]}
    (error, value) = validate(obj, s)
    assert len(error) == 2
    error = dict(error)
    assert "key.[1]" in error
    assert "+int" in error["key.[2]"]
    assert value == {"key": [123, None, None]}


def test_default():
    s = {
        "key": {
            "desc": "datetime",
            "required": True,
            "validate": "datetime",
            "default": datetime.utcnow
        }
    }
    obj = {"key": None}
    (error, value) = validate(obj, s)
    assert not error
    assert isinstance(value["key"], datetime)