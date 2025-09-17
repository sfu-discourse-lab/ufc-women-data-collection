import requests

def get_request(url: str):
    return requests.get(
        url,
        headers={
            # Pretending to request the URL from a Chrome browser to prevent the server from blocking the scraper
            "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36"
        }
    )