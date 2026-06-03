from flask import Blueprint, send_file, render_template_string, request
import json
from pathlib import Path

from .tracker import get_ip, get_country
from .image import generate_image

main = Blueprint('main', __name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = Path('/tmp/data.json')

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (ValueError, FileNotFoundError, OSError):
        return {}

def update_data(country):
    data = load_data()
    data[country] = data.get(country, 0) + 1
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data

@main.route('/')
def home():
    return "Visitor Tracker Running 🚀"
    
@main.route('/debug')
def debug():
    ip = get_ip()
    country = get_country(ip)
    headers = dict(request.headers)
    return f"IP: {ip}<br>Country: {country}<br>Headers: {headers}"
    
@main.route('/track.png')
def track():
    ip = get_ip()
    country = get_country(ip)
    data = update_data(country)
    img_bytes = generate_image(data)
    return send_file(img_bytes, mimetype='image/png')
