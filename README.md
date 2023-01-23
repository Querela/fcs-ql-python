# FCS-QL for Python

* CLARIN-FCS Core 2.0 query language grammar and parser
* based on https://github.com/clarin-eric/fcs-ql
* for more details visit: https://www.clarin.eu/content/federated-content-search-clarin-fcs-technical-details

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
