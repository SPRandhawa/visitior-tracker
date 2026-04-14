import requests
from flask import request


def get_ip():
    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        ip = forwarded.split(',')[0]
    else:
        ip = request.remote_addr or "127.0.0.1"

    return ip.strip()


def get_country(ip):
    if not ip or ip.startswith("127.") or ip in ["localhost", "::1"]:
        return "Local"

    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
        response.raise_for_status()
        res = response.json()

        country = res.get("country_name")

        if not country or country == "":
            return "Unknown"

        return country

    except Exception:
        return "Unknown"
