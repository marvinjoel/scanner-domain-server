import os
from dotenv import load_dotenv

class Config:

    def __init__(self) -> None:
        load_dotenv()
        self.COMPANY_NAME: str = os.getenv("COMPANY_NAME", "Desconocida")
        self.SCAN_INTERVAL: int = int(os.getenv("SCAN_INTERVAL_SECONDS", 3600))
        self.DB_HOST: str = os.getenv("DB_HOST")
        self.DB_USER: str = os.getenv("DB_USER")
        self.DB_PASSWORD: str = os.getenv("DB_PASSWORD")
        self.DB_NAME: str = os.getenv("DB_NAME")
        self.DB_PORT: int = int(os.getenv("DB_PORT", 25060))
        self.DB_SSL_MODE: str = os.getenv("DB_SSL_MODE", "REQUIRED")
        self.SERVER_DIR: str = "/etc/server_web_config"