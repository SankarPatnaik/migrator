"""Core migration logic."""

from __future__ import annotations

from typing import Iterable
from sqlalchemy import create_engine, Table, MetaData, select, insert

from .config import Config, TableMapping


class Migrator:
    """Run table migrations between databases."""

    def __init__(self, config: Config):
        self.config = config

    def migrate_table(self, mapping: TableMapping) -> int:
        """Migrate a single table.

        Returns the number of rows copied.
        """
        src_engine = create_engine(self.config.source_conn)
        tgt_engine = create_engine(self.config.target_conn)

        src_meta = MetaData(bind=src_engine)
        tgt_meta = MetaData(bind=tgt_engine)
        src_table = Table(mapping.source_table, src_meta, autoload_with=src_engine)
        tgt_table = Table(mapping.target_table, tgt_meta, autoload_with=tgt_engine)

        copied = 0
        with src_engine.connect() as src_conn, tgt_engine.begin() as tgt_conn:
            result = src_conn.execute(select(src_table))
            rows: Iterable[dict] = (dict(row) for row in result.mappings())
            batch: list[dict] = []
            for row in rows:
                batch.append(row)
                if len(batch) >= mapping.batch_size:
                    tgt_conn.execute(insert(tgt_table), batch)
                    copied += len(batch)
                    batch.clear()
            if batch:
                tgt_conn.execute(insert(tgt_table), batch)
                copied += len(batch)
        return copied

    def run(self) -> int:
        """Run migrations for all configured tables.

        Returns the total number of rows copied.
        """
        total = 0
        for mapping in self.config.tables:
            total += self.migrate_table(mapping)
        return total
