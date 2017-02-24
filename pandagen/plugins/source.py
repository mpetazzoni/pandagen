# Pandagen

import logging
import os
import re
import StringIO
import yaml

from .. import pandagen


class Source(pandagen.Plugin):
    """
    Add sources to the data processed by Pandagen. If the given source is a
    directory, it will be recursively walked through, adding all files which
    names end with one of the provided extensions (defaults to .md only).
    """

    YAML_DOC_LIMITER = re.compile(r'^---$', re.MULTILINE | re.UNICODE)

    def __init__(self, source='src', exts=['.md']):
        self.source = source
        self.exts = exts

    def _execute(self, pg):
        if os.path.isdir(self.source):
            for root, dirs, files in os.walk(self.source):
                logging.info('Loading %s files from %s/ ...',
                             len(files), root)
                map(lambda f: self._load(pg.data, os.path.join(root, f)),
                    files)
        else:
            logging.info('Loading single file %s ...', self.source)
            self._load(pg.data, self.source)

    def _load(self, data, source):
        if os.path.splitext(source)[1] not in self.exts:
            logging.debug('Skipping %s (extension mismatch).', source)
            return
        dest = source[len(os.path.commonprefix([self.source, source])):]
        if dest.startswith('/'):
            dest = dest[1:]
        data[dest] = self._read(source)
        data[dest]['output'] = dest

    def _read(self, source):
        """Read the given file and generate a resource datum object from it."""
        logging.debug('Reading %s ...', source)
        with open(source) as f:
            _, frontmatter, contents = Source.YAML_DOC_LIMITER.split(f.read())
        datum = {
            'source': source,
            'contents': contents.decode('utf-8').strip(),
        }
        datum.update(yaml.safe_load(StringIO.StringIO(frontmatter)))
        datum['title'] = unicode(datum['title'].strip())
        logging.debug('Read %s%s.', source,
                      u' (`{}`)'.format(datum['title'])
                      if 'title' in datum else '')
        return datum
