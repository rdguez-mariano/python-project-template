# Python Project Template 

This repository provides a python project template to be used with cookiecutter.

## Features

* Dependency and packaging management with [Poetry](https://python-poetry.org/)
* Testing setup with [pytest](https://pytest.org)
* Test coverage using [pytest-cov](https://pypi.org/project/pytest-cov/)
* Automated quality checks with [pre-commit](https://pre-commit.com/)
* Linting with [flake8](https://flake8.pycqa.org/en/latest/)
* Automated formatting with [Black](https://github.com/psf/black)
* Optional [mypy](http://mypy-lang.org/) type checking
* Optional [pydantic](https://pydantic-docs.helpmanual.io/) configuration
* Optional CI/CD Github Action workflow
  * CI: tests, pre-commit checks and documentation building
  * CD: automated semantic versioning and publishing to a python repository
* Optional HTML documentation build with [Sphinx](https://www.sphinx-doc.org/en/master/)

## Prerequisites

To use this template you will first need to install:
- [Git](https://git-scm.com/)
- [Python](https://www.python.org/). To manage your python versions use on of:
    * [pyenv](https://github.com/pyenv/pyenv)
    * [conda](https://www.anaconda.com/)
- [Poetry](https://python-poetry.org/)
- [CookieCutter](https://github.com/cookiecutter/cookiecutter)

## Usage

To create a new project out of this template, simply run:

```bash
cookiecutter https://github.com/rdguez-mariano/python-project-template
```

