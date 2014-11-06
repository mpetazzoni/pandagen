# Pandagen

import jinja2
import logging
import os

from .. import pandagen


class Jinja2(pandagen.Plugin):
    """
    Process a resource through its declared Jinja2 layout template. By default,
    outputs overwrites the 'contents' field.
    """

    def __init__(self, templates, default='layout', into='contents', cache='.cache'):
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates),
            bytecode_cache=jinja2.FileSystemBytecodeCache(cache),
            extensions=['jinja2.ext.with_'])
        self.default = default
        self.into = into

    def _execute(self, pg):
        for v in pg.data.values():
            # Load and render the template.
            template_file = '{}.tmpl'.format(v.get('layout', self.default))
            template = self.env.get_template(template_file)

            context = dict(pg.metadata)
            context.update(v)
            v[self.into] = template.render(context)
