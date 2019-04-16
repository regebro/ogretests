import contextlib
import io
import os
import sys

from unittest import TestCase
from ogretests.main import parse


@contextlib.contextmanager
def redirect_stdout(target):
    original = sys.stdout
    sys.stdout = target
    yield
    sys.stdout = original


class GenericTests(TestCase):
    """Running the basic example from start to end."""

    def test_generic_plugin(self):
        dirname = os.path.split(__file__)[0]
        filename = os.path.join(dirname, 'test_genericplugin.yaml')

        if sys.version_info[0] == 3:
            out = io.StringIO()
        else:
            out = io.BytesIO()
        ogre = parse(filename)
        with redirect_stdout(out):
            with self.assertRaises(SystemExit):
                ogre.run()
        output = out.getvalue()
        self.assertIn('This text should be printed to stdout', output)
        self.assertNotIn('This text should be NOT printed to stdout', output)
