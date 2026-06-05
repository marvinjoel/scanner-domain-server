import requests


class NetworkUtils:

    @staticmethod
    def get_public_ip() -> str:
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=5)
            response.raise_for_status()
            return response.json().get("ip", "Desconocida")
        except requests.RequestException:
            return "Desconocida"


    @staticmethod
    def is_domain_active(domain: str) -> bool:
        try:
            response = requests.get(f"https://{domain}", timeout=5, verify=False)
            return response.status_code < 400
        except requests.RequestException:
            return False