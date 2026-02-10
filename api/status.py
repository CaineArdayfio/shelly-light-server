import requests
from http.server import BaseHTTPRequestHandler

CLOUD_SERVER = "https://shelly-241-eu.shelly.cloud"
AUTH_KEY = "M2Q4MzEwdWlk51C270B23C554CEFDEA595859748D776A1DAEECB25C07B384782DAFAE630D084445AB350A5EE8D4F"
DEVICE_ID = "58e6c50a75b0"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = f"{CLOUD_SERVER}/device/status"
        payload = {"id": DEVICE_ID, "auth_key": AUTH_KEY}

        try:
            response = requests.post(url, json=payload, timeout=10)
            data = response.json()

            if data.get('isok'):
                device_data = data.get('data', {}).get('device_status', {})
                relays = device_data.get('relays', [{}])[0]
                is_on = relays.get('ison', False)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                result = f'{{"success": true, "power": "{("ON" if is_on else "OFF")}"}}'
                self.wfile.write(result.encode())
            else:
                raise Exception()
        except:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"success": false}')
