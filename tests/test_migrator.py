from migrator.config import Config, TableMapping
from migrator.migrator import Migrator
from sqlalchemy import create_engine, text


def setup_db(engine):
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"))
        conn.execute(text("INSERT INTO test (name) VALUES ('a'), ('b')"))


def test_migrate_sqlite(tmp_path):
    src = tmp_path / "src.db"
    tgt = tmp_path / "tgt.db"
    src_engine = create_engine(f"sqlite:///{src}")
    tgt_engine = create_engine(f"sqlite:///{tgt}")
    setup_db(src_engine)
    with tgt_engine.begin() as conn:
        conn.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"))

    cfg = Config(
        source_conn=f"sqlite:///{src}",
        target_conn=f"sqlite:///{tgt}",
        tables=[TableMapping(source_table="test", target_table="test", batch_size=1)],
    )
    migrator = Migrator(cfg)
    copied = migrator.run()
    assert copied == 2
    with tgt_engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM test"))
        assert result.scalar_one() == 2
