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

    class PictureExtension(markdown.extensions.Extension):
        """A Markdown extension that detects paragraphs that only contain a
        picture and annotates them with a special CSS class."""

        def extendMarkdown(self, md, md_globals):
            md.treeprocessors.add('p.img.class',
                                  Markdown.PictureProcessor(md),
                                  '_end')

    class PictureProcessor(markdown.treeprocessors.Treeprocessor):

        def run(self, root):
            for child in root:
                if self.matches(child):
                    child.set('class', 'picture')
                self.run(child)
            return root

        def matches(self, element):
            return element.tag == 'p' and len(element) == 1 and \
                    element.getchildren()[0].tag == 'img'

    def __init__(self, on='contents'):
        self.on = on

    def _execute(self, pg):
        for k, v in pg.data.items():
            if self.on not in v:
                logging.debug('Skipping Markdown tranform on missing ' +
                              'property `%s` of %s.', self.on, k)
                continue
            v[self.on] = markdown.markdown(
                v[self.on], extensions=[Markdown.PictureExtension(),
                                        'markdown.extensions.smarty'])
            logging.debug('Transformed %s:%s as Markdown.', k, self.on)
