# Releasing the pofatu clld app

Install from source:
```shell
git clone https://github.com/pofatu/pofatu
git clone --branch v1.4 --depth 1 https://github.com/pofatu/pofatu-data
cd pofatu
pip install -e .[test]
```
A clone of `pofatu/pofatu-data` is expected in the same directory.
Recreate the database:
```shell
clld initdb development.ini
```
Update the dataset citation in templates/about.mako
Test:
```shell
pytest
```
Store the tested requirements:
```shell
pip freeze > requirements.txt
```
Store a db dump:
```shell
pg_dump -xO --compress gzip:9 pofatu > pofatu.sql.gz
```

