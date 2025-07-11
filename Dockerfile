
FROM python:3.11-slim

WORKDIR /app
COPY smartthings_sonos_multi_zone.py .

RUN pip install requests soco

CMD ["python", "smartthings_sonos_multi_zone.py"]
