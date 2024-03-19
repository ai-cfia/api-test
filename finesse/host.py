import requests

def is_host_up(host_url: str) -> bool:
    health_check_endpoint = f"{host_url}/health"
    try:
        response = requests.get(health_check_endpoint)
        return response.status_code == 200
    except requests.RequestException:
        return False
