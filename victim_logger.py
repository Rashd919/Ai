
import json
import os
from datetime import datetime

VICTIMS_FILE = 'victims.json'

def load_victims():
    if not os.path.exists(VICTIMS_FILE):
        return []
    with open(VICTIMS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_victims(victims):
    with open(VICTIMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(victims, f, indent=4, ensure_ascii=False)

def log_victim_data(ip_address, user_agent, referrer, geo_data=None):
    victims = load_victims()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    victim_entry = {
        'timestamp': timestamp,
        'ip_address': ip_address,
        'user_agent': user_agent,
        'referrer': referrer,
        'geo_data': geo_data
    }
    victims.append(victim_entry)
    save_victims(victims)

def get_victims_data():
    return load_victims()
