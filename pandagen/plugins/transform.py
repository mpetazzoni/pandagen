# Pandagen

import logging
import markdown

from .. import pandagen


class Markdown(pandagen.Plugin):
    """
    Process a given field of each resource as a Markdown document and renders
    it in HTML. By default act on 'contents', which is where a resource's data
    is loaded into.
    """

    def __init__(self, on='contents'):
        self.on = on

    def _execute(self, pg):
        for k, v in pg.data.items():
            if self.on not in v:
                logging.debug('Skipping Markdown tranform on missing ' +
                              'property `%s` of %s.', self.on, k)
                continue
            v[self.on] = markdown.markdown(v[self.on])
