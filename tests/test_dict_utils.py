from unittest import TestCase
from bezalel.impl.dict_utils import *


class TestDictUtils(TestCase):
    def test_dict_get(self):
        assert dict_get({"aa": {"rr": 333, "bb": {"cc": 123, "rrr": 1233}}, "q": 234}, "aa.bb.cc") == 123
        assert dict_get({"aa": {"rr": 333, "bb": {"cc": None, "rrr": 1233}}, "q": 234}, "aa.bb.cc") == None
        assert dict_get({"aa": {"rr": 333, "bb": {"cc": None, "rrr": 1233}}, "q": 234}, "aa.bb.cc", default=-1) == None
        assert dict_get({"aa": {"rr": 333, "bb": {"cc": 123, "rrr": 1233}}, "q": 234}, "aa.bb.cc1") == None
        assert dict_get({"q": 123}, "q") == 123
        assert dict_get({"q": 123}, "a") == None
        assert dict_get({"q": 123}, "a", default=-1) == -1
        assert dict_get({"q": 123}, "a.b.c.d", default=-1) == -1
        assert dict_get({"a": 2134, "q": 123}, "a.b.c.d", default=-1) == -1
        assert dict_get({"a": 2134, "q": 123}, "a.b", default=-1) == -1
        assert dict_get(None, "a.b", default=-1) == -1

    def test_dict_set(self):
        d = {"a": 123, "b": 456}
        dict_set(d, "c", 789)
        self.assertDictEqual({"a": 123, "b": 456, "c": 789}, d)

        d = {"a": 123, "b": 456}
        dict_set(d, "c.d.e", 789)
        self.assertDictEqual({"a": 123, "b": 456, "c": {"d": {"e": 789}}}, d)

        d = {"a": 123, "b": 456, "c": {"r": 44}}
        dict_set(d, "c.d.e", 789)
        self.assertDictEqual({"a": 123, "b": 456, "c": {"r": 44, "d": {"e": 789}}}, d)

        d = {"a": 123, "b": 456, "c": {"r": 44, "d": {"e": 333}}}
        dict_set(d, "c.d.e", 789)
        self.assertDictEqual({"a": 123, "b": 456, "c": {"r": 44, "d": {"e": 789}}}, d)

        d = {"a": 123, "b": 456, "c": 555}
        dict_set(d, "c.d.e", 789)
        self.assertDictEqual({"a": 123, "b": 456, "c": {"d": {"e": 789}}}, d)
