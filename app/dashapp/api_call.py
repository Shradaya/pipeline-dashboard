import requests

def fetch_data(endpoint, params = {}):
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"Request Failed: {e}")
        return None
