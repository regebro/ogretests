import os
import unittest

from ogretests.main import parse

class OgrePluginTests(unittest.TestCase):

    def test_init_plugin(self):
        dirname = os.path.split(__file__)[0]
        filename = os.path.join(dirname, 'test_ogreparser.yaml')
        ogre = parse(filename)
        self.assertIn('Create Tables', ogre.commands)
