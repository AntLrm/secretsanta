import unittest
from secretsanta.secretdraw import secretdraw

class test_secretdraw_methods(unittest.TestCase):

    def test_get_available_names(self):
        msecretdraw = secretdraw()
        msecretdraw.addpeople(['a1',''])
        msecretdraw.addpeople(['a2',''])
        msecretdraw.addpeople(['a3',''])
        msecretdraw.addpeople(['a4',''])
        msecretdraw.addpeople(['a5',''])
        msecretdraw.addpeople(['a6',''])
        msecretdraw.addpeople(['a7',''])
        msecretdraw.addpeople(['a8',''])
        msecretdraw.addpeople(['a9',''])
        msecretdraw.addconstrains([['a1','a2'],['a1','a3'],['a1','a4'],['a4','a1'],['a8','a9']])

        self.assertEqual(msecretdraw.get_available_names(['a1']), ['a5', 'a6', 'a7', 'a8', 'a9'])
        self.assertEqual(msecretdraw.get_available_names(['a2']), ['a1','a3','a4','a5', 'a6', 'a7', 'a8', 'a9'])
        self.assertEqual(msecretdraw.get_available_names(['a1','a2','a8']), ['a3','a4','a5', 'a6', 'a7'])
