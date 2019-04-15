import contextlib
import os
import shutil
import tempfile

from unittest import TestCase
from ogretests.main import Ogre, parse


# Python 2.7 doesn't have a context manager for this, python 3.7 does
@contextlib.contextmanager
def temporary_directory():
    dirname = tempfile.mkdtemp()
    yield dirname
    shutil.rmtree(dirname)


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
        with temporary_directory() as tmpdir:
            # Obviously this shouldn't be hardcoded
            ogre.dump(tmpdir)
            outfile = [name for name in os.listdir(tmpdir) if name.endswith('tbz2')][0]
            ogre.load(os.path.join(tmpdir, outfile))
            print tmpdir
