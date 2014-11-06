# Pandagen

import logging

from .. import pandagen


class Excerpt(pandagen.Plugin):
    """
    Extract the first paragraph of the given field of each resource and set it
    as the 'excerpt' field, removing it from the source field. This is best
    used before any processing on the source field (for example before Markdown
    processing).

    The excerpt can then be individually processed and rendered.
    """

    def __init__(self, on='contents', until='\n\n'):
        self.on = on
        self.until = until

    def _execute(self, pg):
        for k, v in pg.data.items():
            contents = v.get(self.on, '')
            data = contents.split(self.until, 1)
            if len(data) > 1:
                logging.info('Found excerpt on %s (%d bytes).', k,
                             len(data[0]))
                v['excerpt'] = data[0]
            v[self.on] = data[len(data)-1]
