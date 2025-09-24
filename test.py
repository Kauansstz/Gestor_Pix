import requests

url = "https://appws.sandbox.picpay.com/oauth2/token"  # ou produção
payload = {
    "grant_type": "client_credentials",
    "client_id": "0bdba77d-75b2-4bf9-bbfb-db6c59f5bfa1",
    "client_secret": "A6YbbuXgRU4GIkGxCwpLb2g7x1965iUh"
}

response = requests.post(url, json=payload)
print(response.status_code, response.text)
