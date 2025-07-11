
import requests
import soco
import time

# === CONFIGURATION ===
ACCESS_TOKEN = "YOUR_SMARTTHINGS_ACCESS_TOKEN"
CHECK_INTERVAL = 10  # seconds

# === ZONES DEFINITION ===
ZONES = [
    {
        "name": "Bathroom",
        "sensor_id": "YOUR_SENSOR_ID_1",
        "speaker_ip": "192.168.X.X",
        "last_state": None
    },
    {
        "name": "Shower",
        "sensor_id": "YOUR_SENSOR_ID_2",
        "speaker_ip": "192.168.X.X",
        "last_state": None
    }
]

# === SMARTTHINGS HEADERS ===
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

def get_presence(sensor_id):
    url = f"https://api.smartthings.com/v1/devices/{sensor_id}/components/main/capabilities/presenceSensor/status"
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
        return res.json()["presence"]["value"] == "present"
    except Exception as e:
        print(f"[{sensor_id}] Failed to get presence: {e}")
        return None

def mute(ip): soco.SoCo(ip).mute = True
def unmute(ip): soco.SoCo(ip).mute = False

print("🔄 Running multi-zone presence-monitor loop...")
while True:
    for zone in ZONES:
        current = get_presence(zone["sensor_id"])
        if current is None or current == zone["last_state"]:
            continue
        zone["last_state"] = current
        if current:
            print(f"[{zone['name']}] Presence detected → UNMUTE {zone['speaker_ip']}")
            unmute(zone["speaker_ip"])
        else:
            print(f"[{zone['name']}] No presence → MUTE {zone['speaker_ip']}")
            mute(zone["speaker_ip"])
    time.sleep(CHECK_INTERVAL)
