import time
from app.config import Config
from app.database.repository import MySQLRepository
from app.services.monitor import MonitorService


if __name__ == '__main__':
    config = Config()
    repository = MySQLRepository(config)
    service = MonitorService(config, repository)
    
    while True:
        try:
            service.run_scan()
            time.sleep(config.SCAN_INTERVAL)
        except KeyboardInterrupt:
            print("\n[INFO] Monitoreo detenido manualmente.")
            break
        except Exception as e:
            print(f"[ERROR CRÍTICO] {e}")
            time.sleep(60)