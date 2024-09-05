import requests

url = "https://votre-api.com/endpoint"
headers = {
    'Content-Type': 'application/json'
}
payload = {
    "clé1": "valeur1",
    "clé2": "valeur2"
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.json())