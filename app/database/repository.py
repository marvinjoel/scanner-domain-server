import mysql.connector
from app.config import Config


class MySQLRepository:

    def __init__(self, config: Config) -> None:
        self.config = config

    def _get_or_create_server_id(self, cursor, ip: str, disk_free: float) -> int:
        """Inserta o actualiza el servidor incluyendo el espacio en disco libre."""
        server_query = """
            INSERT INTO servers (company_name, server_ip, disk_free_gb)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            company_name = VALUES(company_name),
            disk_free_gb = VALUES(disk_free_gb) -- Se actualiza en cada escaneo
        """
        cursor.execute(server_query, (self.config.COMPANY_NAME, ip, disk_free))
        
        select_query = "SELECT id FROM servers WHERE server_ip = %s"
        cursor.execute(select_query, (ip,))
        result = cursor.fetchone()
        return result[0] if result else None

    def save_domain(self, ip: str, domain: str, is_active: bool, disk_free: float) -> None:
        """Guarda o actualiza el estado del dominio manteniendo la relación estructural."""
        try:
            conn = mysql.connector.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                database=self.config.DB_NAME,
            )
            if conn.is_connected():
                cursor = conn.cursor()
                
                # 1. Asegurar la existencia del servidor y obtener su ID de relación
                server_id = self._get_or_create_server_id(cursor, ip, disk_free)
                
                if not server_id:
                    print(f"[ERROR DB] No se pudo procesar el ID del servidor para la IP {ip}")
                    return

                # 2. Hacer el Upsert del dominio referenciando al servidor
                domain_query = """
                    INSERT INTO domains (server_id, domain_name, is_active)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                    server_id = VALUES(server_id),
                    is_active = VALUES(is_active),
                    last_checked = CURRENT_TIMESTAMP
                """
                cursor.execute(domain_query, (server_id, domain, is_active))
                
                conn.commit()
                cursor.close()
                conn.close()
        except mysql.connector.Error as err:
            print(f"[ERROR DB] {err}")