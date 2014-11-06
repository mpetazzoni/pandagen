# Pandagen

import logging

from .. import pandagen


class Collections(pandagen.Plugin):

    def __init__(self, collection, sortby='source'):
        self.collection = collection
        self.sortby = sortby

    def _execute(self, pg):
        collection = [v for v in pg.data.values()
                      if v.get('collection') == self.collection]
        collection.sort(key=lambda v: v[self.sortby])

        logging.info('Processing collection %s of %d item(s)...',
                     self.collection, len(collection))

        if 'collections' not in pg.metadata:
            pg.metadata['collections'] = {}
        pg.metadata['collections'][self.collection] = collection

        for i, elt in enumerate(collection):
            if i > 0:
                elt['prev'] = collection[i-1]
            if i < len(collection) - 1:
                elt['next'] = collection[i+1]
