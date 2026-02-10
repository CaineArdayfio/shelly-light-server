#!/usr/bin/env python3
"""
Simple Flask server to control Shelly plug via webhooks
Endpoints:
    GET /on - Turn light on
    GET /off - Turn light off
    GET /status - Get light status
"""

from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Shelly configuration
CLOUD_SERVER = "https://shelly-241-eu.shelly.cloud"
AUTH_KEY = "M2Q4MzEwdWlk51C270B23C554CEFDEA595859748D776A1DAEECB25C07B384782DAFAE630D084445AB350A5EE8D4F"
DEVICE_ID = "58e6c50a75b0"

def control_plug(on_state):
    """Control the Shelly plug"""
    url = f"{CLOUD_SERVER}/v2/devices/api/set/switch?auth_key={AUTH_KEY}"
    payload = {"id": DEVICE_ID, "channel": 0, "on": on_state}

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except:
        return False

@app.route('/')
def home():
    return jsonify({
        "message": "Light Control Server",
        "endpoints": {
            "/on": "Turn light on",
            "/off": "Turn light off",
            "/status": "Get light status"
        }
    })

@app.route('/on')
def turn_on():
    success = control_plug(True)
    return jsonify({"success": success, "action": "on"})

@app.route('/off')
def turn_off():
    success = control_plug(False)
    return jsonify({"success": success, "action": "off"})

@app.route('/status')
def status():
    url = f"{CLOUD_SERVER}/device/status"
    payload = {"id": DEVICE_ID, "auth_key": AUTH_KEY}

    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()

        if data.get('isok'):
            device_data = data.get('data', {}).get('device_status', {})
            relays = device_data.get('relays', [{}])[0]
            is_on = relays.get('ison', False)

            return jsonify({"success": True, "power": "ON" if is_on else "OFF"})
    except:
        pass

    return jsonify({"success": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
