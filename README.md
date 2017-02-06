# Pandagen

Pandagen is a plugin pipeline based static content generator. At its
core, Pandagen is an extremely simple plugin execution pipeline that
keeps data and metadata, and passes a reference to itself to each plugin
that it executes.

One of the core use-case for Pandagen is static site generation, in
particular when using the Markdown and Jinja2 plugins. Documents are
expected to be made of the classic YAML front-matter, followed by the
contents.

## Philosophy

The philosophy of Pandagen is before all simplicity in its
implementation (which hopefully will transfer to its simplicity of use
in the future, because it's a bit raw for now!). At its core, Pandagen
simply executes a series of plugins that act on data and metadata kept
by the core and passed to each plugin as it executes.

Plugins have full access to the data and metadata and are free to add,
change and remove entries from them. By assembling plugins, data and
metadata can be loaded from source files, transformed, rendered,
updated, grouped, etc. It is entirely up to the user to define the
pipeline that will generate the desired output, and that freedom is what
makes Pandagen extremely flexible and extensible.

## Usage

For now, using Pandagen involves writing a little bit of Python to chain
the plugins together. In the future, Pandagen will be able to read a
configuration file describing the same thing for people that find it
easier, but having the pipeline described in Python allows for greater
flexibility, as well as the opportunity to write custom plugins and use
them in the pipeline as needed.

### Skeleton

The following snippet of Python can be used as the skeleton for building
and executing a Pandagen pipeline:

```python
#!/usr/bin/env python

from pandagen import Pandagen
from pandagen.plugins import *

(pandagen.Pandagen()
#   .use(...)
    .execute())
```

All the methods of a `Pandagen` instance return the instance itself so
they can be easily chained. It is also possible to execute the pipeline
multiple times after adding plugins (not that this executes the full
pipeline, not just newly added plugins).

For various examples of what Pandagen can do and how plugins are used to
actually make Pandagen do something useful, check out the `examples/`
directory. And because it is probably a very common use case, here's how
to build a blog:

```python
#!/usr/bin/env python

from pandagen import Pandagen
from pandagen.plugins import *

(p = Pandagen()
    # Load all Markdown files from src/, recursively
    .use(source.Source(source='src/', exts=['.md', '.markdown']))
    # Ignore resources that set draft: true
    .use(drafts.Drafts())
    # Parse each resource's tags
    .use(tags.Tags())
    # Generate a slug from each resource's title
    .use(slug.Slug())
    # Render the contents of each resource from Markdown to HTML
    .use(transform.Markdown())
    # Change the output path of each resource to be a permalink. Default
    # pattern is /YYYY/mm/dd/slug-title/
    .use(permalinks.Permalinks())
    # Render each resource through Jinja2 templates according to the
    # resource's layout. Using layout.tmpl as the default.
    .use(templates.Jinja2('templates/'))
    # Clean the output folder. Default is build/
    .use(clean.Clean())
    # Write files to the output folder. Default is build/
    .use(write.Write())
    # Run the pipeline.
    .execute())
```

## Plugin documentation

### Build date

The build date plugin (`pandagen.plugins.build_date.BuildDate`) inserts
the pipeline execution time as a full UTC `datetime` object in the
metadata. By default, the plugin places it under the `builddate` field,
but this can be overridden by passing a different `field` value to the
plugin.

```python
> p = (Pandagen()
    .use(build_date.BuildDate(field='when'))
    .execute())
> p.metadata
{'when': datetime.datetime(2014, 7, 21, 17, 7, 12, 590348)}
```

### Clean

The clean plugin (`pandagen.plugins.clean.Clean`) recursively removes a
directory. It obviously needs to be used with care. By default, the
plugin will remove the `build/` directory, but this can be overridden by
passing a different `target` value to the plugin.

```python
> os.mkdir('foo')
> os.path.isdir('foo')
True
> (Pandagen()
    .use(clean.Clean(target='foo'))
    .execute())
> os.path.isdir('foo')
False
```

### Collections

The collections plugin (`pandagen.plugins.collections.Collections`)
creates a document group of all sources that declare a given
`collection` entry in their metadata. The collection of documents is
then added to the `collections` directory in the pipeline metadata.

Each document in the collection also receives references to the previous
(`prev`) and following (`next`) document in the collection according to
the sort order of the collection.

By default, the plugin will sort by source filename (via the `source`
metadata property of each document) but this can be overridden by
passing a different `sortby` value to the plugin. You can also revert
the sort order by passing `reverse=True`.

```python
# Assuming src/a.md and src/b.md are two documents in the 'blog'
# collection and defining a date.
> p = (Pandagen()
    .use(source.Source())
    .use(collections.Collection('blog', sortby='date'))
    .execute())
> len(p.metadata['collections']['blog'])
2
> a = p.metadata['collections']['blog'][0]
> a['source']
src/a.md
> a['next']['title']
Document B
```

Note that the `prev` and `next` entries are references to other elements
in the collection, which also have `prev` and `next` entries. This means
that the metadata is not acyclic and you should thus be careful when
traversing it.

### Drafts

The drafts plugin (`pandagen.plugins.drafts.Drafts`) removes from the
loaded documents any entry that set `drafts: true` in its front-matter
metadata. It is best used directly after the `source` plugin so that
drafts are not considered by other plugins down the pipeline. The drafts
plugin does not take any arguments.

```python
# Assuming src/post.md and src/draft.md are two documents, the latter
# setting draft: true.
> p = (Pandagen()
    .use(source.Source())
    .execute())
> p.data.keys()
['post.md', 'draft.md']

> p = (Pandagen()
    .use(source.Source())
    .use(drafts.Drafts())
    .execute())
> p.data.keys()
['post.md']
```

### Dump

### Excerpt

### Ignore

### Metadata

### Permalinks

### Reading time

The reading time plugin (`pandagen.plugins.readingtime.ReadingTime`)
computes the expected reading time of each resource and sets it as a
property of that resource. The algorithm considers the number of words
in a given property of each resource and uses an expected
words-per-minute reading speed to computes the reading time. The reading
time is specified as a `datetime.timedelta` object.

The plugin accepts the following parameters:

* `wpm` (defaults to 200), the expected reading speed in words per
  minute -- 200 seems to be a well accepted average;
* `using` (defaults to `contents`), the property in which the resource's
  content is to be found. All resources loaded by the source plugin have
  their body in the `contents`.
* `into` (defaults to `reading_time`), the property of the resource in
  which the plugin will output the reading time.

```python
# Assuming src/post.md is a 1300 words document.
> p = (Pandagen()
    .use(source.Source())
    .use(readingtime.ReadingTime())
    .execute())
> rt = p.data['post.md']['reading_time']
> rt.total_seconds()
390.0
> print("Expected reading time is {:.1f} minute(s)."
        .format(rt.total_seconds() / 60))
Expected reading time is 6.5 minute(s).
```

### Rewrite

### Serve

The serve plugin (`pandagen.plugins.serve.Serve`) spins up Python's
`SimpleHTTPServer` to quickly serve the build output. It is meant to be
used as the last plugin (or one of the last) in the pipeline. The target
will be served forever, until `^C` is pressed, after which the pipeline
continues.

By default the plugin serves the content of the `build/` directory on
port 8000. The served location can be overridden via the `target`
argument, and the port can be changed via the `port` argument.

```python
# This will serve the current directory on port 8080
> Pandagen().use(serve.Serve(target='.', port=8080)).execute()
```

### Slug

### Source

### Static

### Tags

### Templates

### Transform

### Write
