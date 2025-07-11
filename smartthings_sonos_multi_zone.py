
import requests
import soco
import time

# === CONFIGURATION ===
ACCESS_TOKEN = '4ad37261-ab50-49a2-98a2-6ea6447c15e9'
CHECK_INTERVAL = 10  # seconds

# === ZONES DEFINITION ===
ZONES = [
    {
        "name": "Bathroom",
        "sensor_id": "57c2fd5d-b7b6-4322-820f-a02cefd596c9",
        "speaker_ip": "172.16.0.48",
        "last_state": None
    },
    {
        "name": "Shower",
        "sensor_id": "b810fd26-359f-4cb1-9be6-903b4c93a2bf",
        "speaker_ip": "172.16.0.30",
        "last_state": None
    }
]

# === SMARTTHINGS HEADERS ===
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

print("🔄 Running multi-zone presence-monitor loop...")

# Initialize speakers
for zone in ZONES:
    try:
        zone['speaker'] = soco.SoCo(zone['speaker_ip'])
        print(f"🔊 Speaker connected for {zone['name']}")
    except Exception as e:
        zone['speaker'] = None
        print(f"❌ Failed to connect to speaker for {zone['name']}: {e}")

while True:
    for zone in ZONES:
        try:
            # Check SmartThings presence status
            url = f"https://api.smartthings.com/v1/devices/{zone['sensor_id']}/status"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print(f"❌ [{zone['name']}] Error {response.status_code}: {response.text}")
                continue

            data = response.json()
            presence = data['components']['main']['presenceSensor']['presence']['value']

            if presence != zone['last_state']:
                if presence == 'not present':
                    if zone['speaker']:
                        zone['speaker'].mute = True
                    print(f"🔇 [{zone['name']}] No presence – speaker muted.")
                elif presence == 'present':
                    if zone['speaker']:
                        zone['speaker'].mute = False
                    print(f"🔊 [{zone['name']}] Presence detected – speaker unmuted.")
                else:
                    print(f"⚠️ [{zone['name']}] Unknown presence value: {presence}")

                zone['last_state'] = presence
            else:
                print(f"⏳ [{zone['name']}] No change in presence state: {presence}")

        except Exception as e:
            print(f"❌ [{zone['name']}] Exception occurred: {e}")

    time.sleep(CHECK_INTERVAL)
