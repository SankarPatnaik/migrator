# migrator

A simple configuration-driven Python framework to migrate data from
Microsoft SQL Server to ORASS/Oracle databases without business
transformation.

## Usage

1. Create a YAML configuration file:

```yaml
source:
  connection_string: mssql+pyodbc://user:pass@dsn

target:
  connection_string: oracle+cx_oracle://user:pass@host:1521/?service_name=orass

tables:
  - source_table: employees
    target_table: employees
    batch_size: 1000
```

2. Run the migration:

```bash
python -m migrator.cli example_config.yml
```

## Development

Install dependencies and run tests:

```bash
pip install -e .
pytest
```
