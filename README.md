# FCS-QL for Python

- CLARIN-FCS Core 2.0 query language grammar and parser
- based on [Github: clarin-eric/fcs-ql](https://github.com/clarin-eric/fcs-ql)
  and [Github: clarin-eric/fcs-simple-endpoint](https://github.com/clarin-eric/fcs-simple-endpoint)
- for more details visit: [CLARIN FCS Technical Details](https://www.clarin.eu/content/federated-content-search-clarin-fcs-technical-details)


## Installation

```bash
# built package
python3 -m pip install dist/fcs_ql_parser-<version>-py2.py3-none-any.whl
# or
python3 -m pip install dist/fcs-ql-parser-<version>.tar.gz

# for local development
python3 -m pip install -e .
```


## Building

Fetch (or update) grammar files:
```bash
git clone https://github.com/clarin-eric/fcs-ql.git
cp fcs-ql/src/main/antlr4/eu/clarin/sru/fcs/qlparser/*.g4 src/fcsql/
```

(Re-)Generate python parser code:
```bash
# create virtual env
python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel

# install antler tool
python3 -m pip install antlr4-tools
# pip install -e .[antlr]

cd src/fcsql
antlr4 -Dlanguage=Python3 *.g4
```

Build package:
```bash
# pip install -e .[build]
python3 -m build
```


## Development

* Uses `pytest` (with coverage, clarity and randomly plugins).

```bash
python3 -m pip install -e .[test]

pytest
```

Run style checks:
```bash
# general style checks
python3 -m pip install -e .[style]

black --check .
flake8 . --show-source --statistics
isort --check --diff .
mypy src

# building the package and check metadata
python3 -m pip install -e .[build]

python3 -m build
twine check --strict dist/*

# build documentation and check links ...
python3 -m pip install -e .[docs]

sphinx-build -b html docs dist/docs
sphinx-build -b linkcheck docs dist/docs
```


## Build documentation

```bash
python3 -m pip install -r ./docs/requirements.txt
# or 
python3 -m pip install -e .[docs]

sphinx-build -b html docs dist/docs
sphinx-build -b linkcheck docs dist/docs
```


## See also

- [clarin-eric/fcq-ql](https://github.com/clarin-eric/fcs-ql)
- [clarin-eric/fcs-simple-endpoint](https://github.com/clarin-eric/fcs-simple-endpoint)
- [Specification on CLARIN FCS 2.0](https://www.clarin.eu/content/federated-content-search-clarin-fcs-technical-details)
