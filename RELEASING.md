# Releasing the pofatu clld app

- Install from source:
  ```shell
  git clone https://github.com/pofatu/pofatu
  cd pofatu
  pip install -e .[test]
  ```
- A clone of `pofatu/pofatu-data` is expected in the same directory.
- Recreate the database:
  ```shell
  clld initdb development.ini
  ```
- Update the dataset citation in templates/about.mako
- Test:
  ```shell
  pytest
  ```
- Store the tested requirements:
  ```shell
  pip freeze > requirements.txt
  ```
- Store a db dump:
  ```shell
  pg_dump -xO pofatu > pofatu.sql
  zip pofatu.sql.zip pofatu.sql
  rm pofatu.sql
  ```

