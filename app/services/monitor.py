import time
import requests
from app.config import Config
from app.database.repository import MySQLRepository
from app.utils.network import NetworkUtils
from app.utils.nginx import NginxExtractor
from app.utils.apache import ApacheExtractor
from app.utils.system import SystemUtils


class MonitorService:

    def __init__(self, config: Config, repo: MySQLRepository) -> None:
        self.config = config
        self.repo = repo
        requests.packages.urllib3.disable_warnings() 

    def run_scan(self) -> None:
        """ NginxExtractor usa Nginx, ApacheExtractor usa Apache, solo cambiar esa linea """
        print(f"\n[INFO] Iniciando escaneo - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        public_ip = NetworkUtils.get_public_ip()
        disk_free = SystemUtils.get_disk_free_gb() 
        print(f"[INFO] Espacio libre en disco: {disk_free} GB")
        domains = NginxExtractor.get_domains(self.config.NGINX_DIR)
        #domains = ApacheExtractor.get_domains(self.config.SERVER_DIR)
        
        for domain in domains:
            is_active = NetworkUtils.is_domain_active(domain)
            self.repo.save_domain(public_ip, domain, is_active, disk_free)
            estado = "🟢" if is_active else "🔴"
            print(f"{estado} Procesado: {domain}")
            
        print("[INFO] Escaneo finalizado. Esperando al siguiente ciclo...")