import shutil

class SystemUtils:
    
    @staticmethod
    def get_disk_free_gb() -> float:
        """Obtiene el espacio libre en el disco del host en Gigabytes."""
        try:
            total, used, free = shutil.disk_usage("/host")
            free_gb = free / (1024 ** 3)
            return round(free_gb, 2)
        except Exception as e:
            print(f"[ERROR SO] No se pudo leer el espacio en disco: {e}")
            return 0.0