# Contributing

## Documentation

This project uses Sphinx to build its documentation and present it in HTML format.

Simply run:
```bash
$ cd docs
$ make html
```

```bash
Running Sphinx
...
build succeeded.
The HTML pages are in _build/html.
```

Inside the `docs/` directory, a new directory `_build/html` is created. It contains our built documentation as HTML files. Open `_build/html/index.html` to see the landing page.

## Pre-commit

Pre-commit is a tool allowing some quality checks to be run before each commit.

In order for Git to run these checks, you first need to register the pre-commit hooks with:

```bash
pre-commit install
```

To run all hooks on all files, simply run:

```bash
pre-commit run --all-files
```

For more info, make sure to check out Pre-commit's [documentation](https://pre-commit.com/).

## Testing

To run the tests:

```bash
poetry run pytest
```

To compute test coverage, add the `--cov` parameter:

```bash
poetry run pytest --cov {{ cookiecutter.pkg_shelf }}.{{ cookiecutter.pkg_name }}
```

This will generate a report saved as a `.coverage` file.
