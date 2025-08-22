"""Command line interface for migration framework."""

from __future__ import annotations

import argparse

from .config import Config
from .migrator import Migrator


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate tables between databases")
    parser.add_argument("config", help="Path to YAML configuration file")
    args = parser.parse_args()

    cfg = Config.from_file(args.config)
    migrator = Migrator(cfg)
    total = migrator.run()
    print(f"Copied {total} rows")


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    main()
