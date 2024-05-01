import urllib.parse
import webbrowser
import requests
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

def handle_callback(client_id, client_secret, callback_url, code):
    tokenUrl = "https://developer.api.autodesk.com/authentication/v2/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": callback_url
    }
    resp = requests.post(tokenUrl, data=payload)
    respJson = resp.json()
    print("Authenticated successfully. Token:", respJson)
    return respJson

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        code = params.get('code', [''])[0]
        if code:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authentication successful. You can close this window now.")
            handle_callback(CLIENT_ID, CLIENT_SECRET, CALLBACK_URL, code)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad Request")

def start_callback_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CallbackHandler)
    print(f'Starting callback server on port {port}...')
    httpd.handle_request()

def initiate_authentication(client_id, callback_url, scopes):
    auth_url = f"https://developer.api.autodesk.com/authentication/v2/authorize?response_type=code&client_id={client_id}&redirect_uri={callback_url}&scope={scopes}"
    webbrowser.open(auth_url)

# Usage
CLIENT_ID = os.environ.get('APS_CLIENT_ID')
CLIENT_SECRET = os.environ.get('APS_CLIENT_SECRET')
CALLBACK_URL = 'http://localhost:8080/api/auth/callback'
SCOPES = 'data:read viewables:read'

initiate_authentication(CLIENT_ID, CALLBACK_URL, SCOPES)
start_callback_server()
