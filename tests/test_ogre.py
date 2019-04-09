from io import StringIO
from unittest import TestCase
from yaml import safe_load

from ogretests.main import Ogre

class OgreTests(TestCase):

    def test_init(self):
        options = {'name': 'test', 'actions': []}
        o = Ogre(options)
        self.assertEqual(o.name, 'test')
        self.assertEqual(o.actions, [])

    def test_unknown_option(self):
        options = {'name': 'test', 'actions': [], 'notanoption': 'error'}
        with self.assertRaises(KeyError):
            Ogre(options)
