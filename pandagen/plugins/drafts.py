# Pandagen

import logging

from .. import pandagen


class Drafts(pandagen.Plugin):
    """
    Ignore resources that declare themselves a draft in their YAML
    front-matter.
    """

    def _execute(self, pg):
        for k, v in pg.data.items():
            if v.get('draft', False):
                logging.info('Ignoring draft %s%s.',
                             k, ' (`{}`)'.format(v['title'])
                                if 'title' in v else '')
                del pg.data[k]
