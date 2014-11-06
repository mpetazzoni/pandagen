# Pandagen

import logging

from .. import pandagen


class Tags(pandagen.Plugin):
    """
    Parse tags declared in the front-matter of the loaded resources. Tags can
    be declared as a mix of comma-separated or space-separated items, or as a
    YAML list of those. The plugin will correctly parse and expand all of them.
    All found tags are also added, with their number of occurences, to the
    global set of tags in the metadata (useful to build a tag cloud for
    example).
    """

    def _execute(self, pg):
        pg.metadata['tags'] = pg.metadata.get('tags', {})

        for k, v in pg.data.items():
            tags = self._as_list(v.get('tags'))
            for tag in tags:
                pg.metadata['tags'][tag] = pg.metadata['tags'].get(tag, 0) + 1
            v['tags'] = tags
            logging.debug('Tags for %s are: %s.', k, tags)
