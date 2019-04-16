import datetime
import imp
import logging
import os
import tarfile
from collections import defaultdict


import yaml


class NameConflictError(NameError):
    pass


class Ogre(object):

    def __init__(self, options):
        self.name = options.pop('name')
        self.actions = options.pop('actions')
        self.plugins = {}
        self.commands = {}

        if options:
            # Unhandled options
            raise KeyError("Unknown Ogre options: %s" % ', '.join(options.keys()))

    def add_plugin(self, module):
        # XXX implement namespaces
        plugin = module.ogre_plugin
        # XXX verify that plugin names doesn't clash
        if plugin.name in self.plugins:
            raise NameConflictError('A plugin called %s has already been loaded.' % plugin.name)
        self.plugins[plugin.name] = plugin

        for name, function in plugin.actions.items():
            if name in self.commands:
                raise NameConflictError('%s is already defined in another module' % name)
            self.commands[name] = function

    def run(self):
        for action in self.actions:
            if isinstance(action, dict):
                # Action with parameters:
                action_name = next(iter(action.keys()))
                method = self.commands[action_name]
                method(**action[action_name])
            elif isinstance(action, str):
                try:
                    method = self.commands[action]
                except KeyError:
                    raise KeyError('Unknown action "%s"' % action)
                method()
            else:
                raise SyntaxError('Unknown action type of action "%s"' % action)

    def dump(self, directory_path):
        dt = datetime.datetime.now()
        timestamp = dt.strftime('%Y%m%d-%H%M%S')
        filename = os.path.join(directory_path, 'ogrehouse-%s.tbz2' % timestamp)

        house = tarfile.open(filename, 'w:bz2')
        for plugin in self.plugins.values():
            for fn, stream in plugin.dump():
                tarname = os.path.join(plugin.name, fn)
                ti = tarfile.TarInfo(tarname)
                # Get size
                ti.size = stream.seek(0, 2)
                # Move to beginning of stream
                stream.seek(0)
                # Add file to tar
                house.addfile(ti, stream)

    def load(self, filename):
        house = tarfile.open(filename, 'r')
        files = defaultdict(dict)

        for fn in house.getnames():
            pluginname, filename = os.path.split(fn)
            if pluginname not in self.plugins:
                raise NameError('Plugin "%s" not found' % pluginname)
            stream = house.extractfile(fn)
            files[pluginname][filename] = stream

        for pluginname, plugin in self.plugins.items():
            if pluginname not in files:
                logging.getLogger('ogre').warn("Plugin '%s' has no data to load" % pluginname)
            else:
                plugin.load(files[pluginname])


class OgreParser(object):

    def parse(self, path):
        with open(path, 'rt') as ogrefile:
            options = yaml.safe_load(ogrefile)

        directory, ignore = os.path.split(path)
        plugins = options.pop('plugins')

        ogre = Ogre(options)
        for modulename in plugins:
            if modulename[0] == '.':
                modulename = modulename[1:]
                searchpath = [directory]
            else:
                searchpath = None
            for name in modulename.split('.'):
                moduleinfo = imp.find_module(name, searchpath)
                module = imp.load_module(name, *moduleinfo)
                if hasattr(module, '__path__'):
                    searchpath = module.__path__
            ogre.add_plugin(module)

        return ogre


parse = OgreParser().parse
