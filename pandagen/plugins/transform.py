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

    class PictureParagExtension(markdown.extensions.Extension):
        """A Markdown extension that detects paragraphs that only contain a
        picture and annotates them with a special CSS class."""

        def extendMarkdown(self, md, md_globals):
            md.treeprocessors.add('p.img.class',
                                  Markdown.PictureParagProcessor(md),
                                  '_end')

    class PictureParagProcessor(markdown.treeprocessors.Treeprocessor):

        def run(self, root):
            for child in root:
                if self.matches(child):
                    child.set('class', 'picture')
                self.run(child)

        def matches(self, element):
            return element.tag == 'p' and len(element) == 1 and \
                    element.getchildren()[0].tag == 'img' and \
                    not element.getchildren()[0].tail

    class PictureFloatExtension(markdown.extensions.Extension):
        """A Markdown extension that sets the left/right CSS class on images
        with that attribute (as extracted by the attr_list extension)."""

        def extendMarkdown(self, md, md_globals):
            md.treeprocessors.add('img.float',
                                  Markdown.PictureFloatProcessor(md),
                                  '_end')

    class PictureFloatProcessor(markdown.treeprocessors.Treeprocessor):

        def run(self, root):
            for child in root:
                if child.tag == 'img':
                    side = child.get('left') or child.get('right')
                    if side:
                        child.set('class', side)
                self.run(child)

    def __init__(self, on='contents'):
        self.on = on
        logging.getLogger('MARKDOWN').setLevel(logging.INFO)

    def _execute(self, pg):
        for k, v in pg.data.items():
            if self.on not in v:
                logging.debug('Skipping Markdown tranform on missing ' +
                              'property `%s` of %s.', self.on, k)
                continue
            v[self.on] = markdown.markdown(
                    v[self.on], output_format='html5',
                    extensions=[
                        Markdown.PictureParagExtension(),
                        Markdown.PictureFloatExtension(),
                        'markdown.extensions.attr_list',
                        'markdown.extensions.smarty'])
            logging.debug('Transformed %s:%s as Markdown.', k, self.on)
