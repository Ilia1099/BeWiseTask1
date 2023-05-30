from pathlib import Path

from pydantic import BaseSettings, PostgresDsn, SecretStr


class ConfigTest(BaseSettings):
    db_protocol: str = "sqlite+aiosqlite"
    path_to_file: Path = Path('test_db.sqlite3').absolute().resolve()

    def db_dsn(self, protocol=None) -> PostgresDsn | str:
        protocol = protocol or self.db_protocol
        return f"{self.db_protocol}///{self.path_to_file}"