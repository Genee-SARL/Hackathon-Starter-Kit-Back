from typing import Final
import os


class BaseConfig:
    """Configuration common to all modes (test, dev, prod)"""

    def __init__(self):
        # Flask
        self.MIGRATION: Final[str] = os.getenv("MIGRATION")

        # Database
        self.USER: Final[str] = os.getenv("DB_USER")
        self.DB_PASS: Final[str] = os.getenv("DB_PASS")
        self.DB_NAME: Final[str] = os.getenv("DB_NAME")
        self.DB_IP: Final[str] = os.getenv("DB_IP")
        self.SQLALCHEMY_DATABASE_URI: Final[str] = \
            f"postgresql://{self.USER}:{self.DB_PASS}@localhost:5432/{self.DB_NAME}?client_encoding=utf8"
        print(self.SQLALCHEMY_DATABASE_URI)


class TestingConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.DEBUG = True
        self.ENV = "test"


class DevelopmentConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.DEBUG = True
        self.ENV = "dev"


class ProductionConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.DEBUG = False
        self.ENV = "prod"
