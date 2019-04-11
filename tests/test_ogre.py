import os

from unittest import TestCase

from ogretests.main import Ogre, parse


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


class IntegrationTests(TestCase):
    """Running the basic example from start to end."""

    def test_run(self):
        dirname = os.path.split(__file__)[0]
        filename = os.path.join(dirname, 'test_ogreparser.yaml')
        ogre = parse(filename)

        ogre.run()
        # Obviously this shouldn't be hardcoded
        ogre.dump('/tmp')
        ogre.load('/tmp/ogrehouse-20190411-145812.tbz2')
