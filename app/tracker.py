import requests
from flask import request

def get_ip():
    for header in ['X-Forwarded-For', 'X-Real-IP', 'CF-Connecting-IP']:
        ip = request.headers.get(header)
        if ip:
            return ip.split(',')[0].strip()
    return request.remote_addr or "127.0.0.1"

def get_country(ip):
    if not ip or ip == "::1":
        return "Unknown"
    try:
        response = requests.get(
            f"http://ip-api.com/json/{ip}?fields=country,countryCode",
            timeout=3
        )
        res = response.json()
        if res.get("country"):
            country = res["country"]
            code = res.get("countryCode", "")
            flag = ''.join(chr(0x1F1E0 + ord(c) - ord('A')) for c in code.upper()) if code else ""
            return f"{flag} {country}"
        return "Unknown"
    except:
        return "Unknown"
