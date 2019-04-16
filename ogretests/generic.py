# Generic commands


def _print(text):
    print(text)


def _error(error):
    raise SystemExit(error)


class OgrePlugin(object):
    name = 'ogretests.generic'

    actions = {
        "Print": _print,
        "Error": _error,
    }

    def dump(self):
        # No data retained by this plugin
        return StopIteration

    def load(self, streams):
        # No data retained by this plugin
        pass


ogre_plugin = OgrePlugin()
