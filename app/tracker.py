import requests
from flask import request

def get_ip():
    # Render passes real IP in these headers
    for header in ['X-Forwarded-For', 'X-Real-IP', 'CF-Connecting-IP']:
        ip = request.headers.get(header)
        if ip:
            return ip.split(',')[0].strip()
    return request.remote_addr or "127.0.0.1"

def get_country(ip):
    if not ip or ip == "::1":
        return "Unknown"
    try:
        # Use ip-api.com instead - more reliable & free
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

    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
        response.raise_for_status()
        res = response.json()
        country = res.get("country_name", "Unknown")
        emoji = res.get("country_code", "")
        # Convert country code to flag emoji
        flag = ''.join(chr(0x1F1E0 + ord(c) - ord('A')) for c in emoji.upper()) if emoji else "🌐"
        return f"{flag} {country}"
    except (requests.RequestException, ValueError):
        return "🌐 Unknown"
