import imp
import os

import yaml


class Ogre(object):

    def __init__(self, options):
        self.name = options.pop('name')
        self.actions = options.pop('actions')
        self.commands = {}

        if options:
            # Unhandled options
            raise KeyError("Unknown Ogre options: %s" % ', '.join(options.keys()))

    def add_library(self, module):
        # XXX implement namespaces
        for name, function in module.init_ogreplugin().items():
            if name in self.commands:
                raise NameConflictError('%s is already defined in another module' % name)
            self.commands[name] = function


class OgreParser(object):

    def parse(self, path):
        with open(path, 'rt') as ogrefile:
            options = yaml.safe_load(ogrefile)

        directory, name = os.path.split(path)
        plugins = options.pop('plugins')

        ogre = Ogre(options)
        for modulename in plugins:
            if modulename[0] == '.':
                modulename = modulename[1:]
                searchpath = [directory]
            else:
                searchpath = None
            moduleinfo = imp.find_module(modulename, searchpath)
            module = imp.load_module(modulename, *moduleinfo)
            ogre.add_library(module)

        return ogre


parse = OgreParser().parse


class Action(object):

    def __init__(self, action, parameters):
        self.action = action
        self.parameters = parameters

    def run(self):
        self.action(**parameters)


#class Actions - container for Action objects

# class Library, the module that contains the functions
