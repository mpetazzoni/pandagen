# Pandagen

import logging


class Pandagen:
    """
    Core Pandagen pipeline executor.
    """

    def __init__(self):
        self._plugins = []

    def use(self, plugin):
        self._plugins.append(plugin)
        return self

    def execute(self):
        self.data = {}
        self.metadata = {}
        map(lambda p: p.run(self), self._plugins)
        return self


class Plugin:
    """
    Base plugin class. Plugins need to extend this base class and implement the
    _execute() method.
    """

    def run(self, pg):
        logging.debug('---> Plugin %s on %d source(s).',
                      self.__class__.__name__, len(pg.data))
        self._execute(pg)
        logging.debug('<--- Plugin %s done, now with %d source(s).',
                      self.__class__.__name__, len(pg.data))

    def _execute(self, pg):
        raise NotImplementedError

    def _as_list(self, v):
        """Parses the given value, potentially comma-separated, and returns it
        as a list of distinct elements."""
        v = v or []
        if type(v) is str:
            v = [v]

        v = map(lambda s: s.replace(',', ' ').split(), v)
        return filter(None, reduce(sum, v, []))
