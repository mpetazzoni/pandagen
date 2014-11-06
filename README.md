# Pandagen

Pandagen is a plugin pipeline based static content generator. At its
core, Pandagen is an extremely simple plugin execution pipeline that
keeps data and metadata, and passes a reference to itself to each plugin
that it executes.

Plugins have full access to the data and metadata and are free to add,
change and remove entries from them. By assembling plugins, data and
metadata can be loaded from source files, transformed, rendered,
updated, grouped, etc.

One of the core use-case for Pandagen is static site generation, in
particular when using the Markdown and Jinja2 plugins. Documents are
expected to be made of the classic YAML front-matter, followed by the
contents.

## Usage

For now, using Pandagen involves writing a little bit of Python to chain
the plugins together. In the future, Pandagen will be able to read a
configuration file describing the same thing. A basic pipeline would
look like this:

```python
#!/usr/bin/env python

from pandagen import Pandagen
from pandagen.plugins import *

p = Pandagen()

# Load all Markdown files from src/, recursively
p.use(source.Source(source='src/', exts=['.md', '.markdown']))

# Ignore resources that set draft: true
p.use(drafts.Drafts())

# Parse each resource's tags
p.use(tags.Tags())

# Generate a slug from each resource's title
p.use(slug.Slug())

# Render the contents of each resource from Markdown to HTML
p.use(transform.Markdown())

# Change the output path of each resource to be a permalink. Default
# pattern is /YYYY/mm/dd/slug-title/
p.use(permalinks.Permalinks())

# Render each resource through Jinja2 templates according to the
# resource's layout. Using layout.tmpl as the default.
p.use(templates.Jinja2('templates/'))

# Clean the output folder. Default is build/
p.use(clean.Clean())

# Write files to the output folder. Default is build/
p.use(write.Write())

# Run the pipeline.
p.execute()
```

## Plugin documentation


