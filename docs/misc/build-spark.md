# Build Spark

## Doc

### Cannot uninstall six
Cannot uninstall 'six'. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall.

```
sudo pip install six --upgrade --ignore-installed six
```

### sphinx-build command not found
The 'sphinx-build' command was not found.

```
sudo pip install Sphinx --upgrade --ignore-installed Sphinx
```

### build log

```
Moving to project root and building API docs.
Running 'build/sbt -Pkinesis-asl clean compile unidoc' from
...
[info] Main Java API documentation successful.
...
[info] Main Scala API documentation successful.
...
Moving back into docs dir.
Removing old docs

Making directory api/scala
cp -r ../target/scala-2.11/unidoc/. api/scala
Making directory api/java
cp -r ../target/javaunidoc/. api/java
...
Moving to python/docs directory and building sphinx.
...
Build finished. The HTML pages are in _build/html.
Moving back into docs dir.
Making directory api/python
cp -r ../python/docs/_build/html/. api/python
Moving to R directory and building roxygen docs.
...
Moving back into docs dir.
Making directory api/R
cp -r ../R/pkg/html/. api/R
cp ../R/pkg/DESCRIPTION api
Moving to project root and building API docs.
...
Moving back into docs dir.
Moving to SQL directory and building docs.
Generating markdown files for SQL documentation.
...
Moving back into docs dir.
Making directory api/sql
cp -r ../sql/site/. api/sql
...
            Source: /path/to/spark/docs
       Destination: /path/to/spark/docs/_site
 Incremental build: disabled. Enable with --incremental
      Generating...
```

