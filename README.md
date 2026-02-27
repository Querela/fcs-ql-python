# FCS-QL for Python

<!-- START: BADGES -->

[![](https://img.shields.io/badge/%20code%20style-black-000000)](https://github.com/psf/black)
[![](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)
[![](https://img.shields.io/badge/linting-flake8-yellowgreen)](https://github.com/PyCQA/flake8)  
[![](https://img.shields.io/badge/%20formatter-docformatter-fedcba.svg)](https://github.com/PyCQA/docformatter)
[![](https://img.shields.io/badge/%20doc%20style-sphinx-0a507a.svg)](https://www.sphinx-doc.org/en/master/usage/index.html)
[![](https://img.shields.io/badge/%20doc%20style-google-3666d6.svg)](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings)  
[![fcs-ql-parser @ PyPI](https://img.shields.io/pypi/v/fcs-ql-parser)](https://pypi.python.org/pypi/fcs-ql-parser)
[![CI: Python package](https://github.com/Querela/fcs-ql-python/actions/workflows/python-package.yml/badge.svg)](https://github.com/Querela/fcs-ql-python/actions/workflows/python-package.yml)
[![](https://img.shields.io/github/last-commit/Querela/fcs-ql-python)](https://github.com/Querela/fcs-ql-python/commits/main)
[![Documentation Status](https://readthedocs.org/projects/fcs-ql-python/badge/?version=latest)](https://fcs-ql-python.readthedocs.io/en/latest/?badge=latest)

<!-- END: BADGES -->

- CLARIN-FCS Core 2.0 query language grammar and parser
- based on [Github: clarin-eric/fcs-ql](https://github.com/clarin-eric/fcs-ql)
  and [Github: clarin-eric/fcs-simple-endpoint](https://github.com/clarin-eric/fcs-simple-endpoint)
- for more details visit: [CLARIN FCS Technical Details](https://www.clarin.eu/content/federated-content-search-clarin-fcs-technical-details)

## Installation

Install from PyPI:

```bash
python3 -m pip install fcs-ql-parser
```

Or install from source:

```bash
git clone https://github.com/Querela/fcs-ql-python.git
cd fcs-ql-python
uv build

# built package
python3 -m pip install dist/fcs_ql_parser-<version>-py3-none-any.whl
# or
python3 -m pip install dist/fcs_ql_parser-<version>.tar.gz

# for local development
python3 -m pip install -e .
```

## Usage

## Development

Fetch (or update) grammar files:

```bash
git clone https://github.com/clarin-eric/fcs-ql.git
cp fcs-ql/src/main/antlr4/eu/clarin/sru/fcs/qlparser/fcs/*.g4 src/fcsql/
```

(Re-)Generate python parser code:

```bash
# setup environment
uv sync --extra antlr
# NOTE: you can activate the environment (if you do not want to prefix everything with `uv run`)
# NOTE: `uv` does not play nicely with `pyenv` - if you use `pyenv`, sourcing does NOT work!
source .venv/bin/activate

cd src/fcsql
uv run antlr4 -Dlanguage=Python3 *.g4 -listener -visitor
```

Run style checks:

```bash
# setup environment
uv sync --extra style

uv run black --check .
uv run flake8 . --show-source --statistics
uv run isort --check --diff .

uv run mypy src
```

Run tests (`pytest` with coverage, clarity and randomly plugins):

```bash
# setup environment
uv sync --extra test

uv run pytest
# to see output and run a specific test file
uv run pytest -v -rP tests/validation/test_validation.py
```

Build documentation:

```bash
# setup environment
uv sync --extra docs
# or if standalone
python3 -m pip install -r ./docs/requirements.txt

# build documentation and check links ...
uv run sphinx-build -b html docs dist/docs
uv run sphinx-build -b linkcheck docs dist/docs
```

Run check before publishing:

```bash
# setup environment
uv sync --extra build

# build the package
uv build
# run metadata check
# uv run python3 -m build
uv run twine check --strict dist/*
# (manual) check of package contents
tar tvf dist/fcs_ql_parser-*.tar.gz
```

## See also

- [clarin-eric/fcq-ql](https://github.com/clarin-eric/fcs-ql)
- [clarin-eric/fcs-simple-endpoint](https://github.com/clarin-eric/fcs-simple-endpoint)
- [Specification on CLARIN FCS 2.0](https://www.clarin.eu/content/federated-content-search-clarin-fcs-technical-details)
