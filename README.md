# SmartThings-Sonos Auto-Mute System 🤖🔊

Python-based smart home automation project that mutes/unmutes Sonos speakers in response to presence detection via Aqara FP1 sensors, using Samsung SmartThings API.

## 🧠 Project Summary

This system automates Sonos speaker behavior in zones like bathrooms and showers. When a zone is empty, the speaker is muted; when presence is detected, it's unmuted — all via local network and SmartThings API.

## ✅ Features

- Multi-zone support (e.g., Bathroom, Shower, etc.)
- Real-time presence detection via Aqara FP1 sensors
- Mute/unmute Sonos speakers using SoCo (LAN)
- Dockerized and deployable on Synology NAS (DSM/Container Manager)
- Background service, runs 24/7 reliably
- Auto-start on reboot (optional via Container settings)

## 🛠️ Technologies

- Python 3.x
- SmartThings REST API
- [SoCo](https://github.com/SoCo/SoCo) (Sonos Control via LAN)
- Docker & Docker Compose
- Synology DSM (tested on DS920+)

## 📁 Project Structure

```
.
├── smartthings_sonos_multi_zone.py   # Main logic
├── Dockerfile                         # Container image definition
├── docker-compose.yml                 # Service orchestration
└── README.md                          # This file
```

## ⚙️ Configuration

### 1. Clone the repo

```bash
git clone https://github.com/aputze/smartthings-sonos-auto-mute.git
cd smartthings-sonos-auto-mute
```

### 2. Set SmartThings credentials

- Go to [SmartThings API](https://account.smartthings.com/tokens) and create a token
- Ensure it has these permissions:
  - `Devices: Read`
  - `Devices: Execute Commands`

Edit `smartthings_sonos_multi_zone.py`:

```python
ACCESS_TOKEN = "your-smartthings-token"
ZONES = [
    {
        "name": "Bathroom",
        "sensor_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "speaker_ip": "192.168.1.100"
    },
    {
        "name": "Shower",
        "sensor_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "speaker_ip": "192.168.1.101"
    }
]
```

### 3. Run via Docker

```bash
docker-compose up -d
```

Or deploy on your **Synology NAS** via **Container Manager**:

- Go to Projects → Create
- Upload folder and select `docker-compose.yml`
- Set network mode: `host`
- Enable auto-restart

## 🧪 Example Output

When presence is detected:

```
[Bathroom] Presence: True → Unmuting 192.168.1.100
[Shower]   Presence: False → Muting 192.168.1.101
```

## 📸 Optional: Screenshots / GIF

*Coming soon*

## 📜 License

MIT License — feel free to fork, modify, contribute.

## 🙋‍♂️ Author

Built by [Sergei Lerner](https://www.linkedin.com/in/sergei-lerner-b5757837/)
