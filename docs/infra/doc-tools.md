# Doc Tools

## Overview

## Design and Implementation
_config.yml

```
highlighter: rouge
```

include_example.rb

```
require 'rouge'

rendered_code = Rouge.highlight(code, @lang, 'html')
```

README.md

```
$ sudo gem install jekyll jekyll-redirect-from rouge
```

## Issues
### Jekyll Pygments
Spark project uses Jekyll to generate documentations. pygments.rb is used as the syntax highligter. pygments.rb is a Ruby wrapper for the Python pygments syntax highlighter. Because [pygments.rb requires Python 2.x](https://github.com/tmm1/pygments.rb/issues/152), we just fail if we build docs in a Python 3.x environment. Actually, Jekyll already [switched from pygments.rb to Rouge as the default syntax highlighter](https://github.com/jekyll/jekyll/pull/3323) for long (over 3 years ago since Jekyll 3.0). Furthermore, Jekyll 4.0 (the next Jekyll release) will [drop support for pygments as syntax-highlighter](https://github.com/jekyll/jekyll/pull/7118).

This PR aims to switch from pygments.rb to Rouge as the syntax highligter.

pygments.rb/Rouge highlight API doc:
* [pygments.highlight](http://pygments.org/docs/api/?highlight=highlight)
* [Rouge.highlight](https://www.rubydoc.info/gems/rouge/Rouge.highlight)

Althoug we can easily work around this by creating a Python 2.x via conda env or virtualenv. Given that Python 2.x will reach its EOL soon and Python 3.x is becoming mainstream.
