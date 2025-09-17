import requests

def get_request(url: str):
    return requests.get(
        url,
        headers={
            # Pretending to request the URL from a Chrome browser to prevent the server from blocking the scraper
            "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36"
        }
    )


def get_page_name(page_link: str):
    page_name = page_link.replace("/", "_")

    if page_name.startswith("_"):
        page_name = page_name[1:]

    return page_name


def get_image_name(image_src: str):
    return image_src\
        .split("/")[-1]\
        .split("?")[0]
