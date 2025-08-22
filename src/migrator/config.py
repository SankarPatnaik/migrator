"""Configuration utilities for migration framework."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List
import yaml


@dataclass
class TableMapping:
    """Mapping between source and target tables."""

    source_table: str
    target_table: str
    batch_size: int = 1000


@dataclass
class Config:
    """Configuration for a migration job."""

    source_conn: str
    target_conn: str
    tables: List[TableMapping]

    @classmethod
    def from_file(cls, path: str | Path) -> "Config":
        """Load configuration from a YAML file."""
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        tables = [TableMapping(**tbl) for tbl in data.get("tables", [])]
        return cls(
            source_conn=data["source"]["connection_string"],
            target_conn=data["target"]["connection_string"],
            tables=tables,
        )
