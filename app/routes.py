from flask import Blueprint, send_file
import json
from pathlib import Path

from .tracker import get_ip, get_country
from .image import generate_image

main = Blueprint('main', __name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data.json"
STATS_FILE = BASE_DIR / "stats.png"

def update_data(country):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (ValueError, FileNotFoundError, OSError):
        data = {}

    data[country] = data.get(country, 0) + 1

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return data


@main.route('/')
def home():
    return "Visitor Tracker Running 🚀"

@main.route('/track.png')
def track():
    ip = get_ip()
    country = get_country(ip)
    data = update_data(country)
    img = generate_image(data, STATS_FILE)
    return send_file(img, mimetype='image/png')