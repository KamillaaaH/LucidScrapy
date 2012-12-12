#!/usr/bin/python
# -*- coding: utf-8 *-*
__author__="kamilla"
__date__ ="$Dec 10, 2012 11:58:46 PM$"

import unittest
from pages import CreateJSFile

class TestCreateJSFile:

    def setUp(self):
        self.data = {"value1": "1", "value2": "2", "value3": "3"}
        self.total = 6

    def test_CreateJSFile(self):
        data = self.data
        self.assertEqual(self.total, CreateJSFile.calculateTotal(data))


if __name__ == "__main__":
    unittest.main()