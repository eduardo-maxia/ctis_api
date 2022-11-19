import requests

url = "https://api.pagar.me/core/v5/orders"

headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, headers=headers)

print(response.text)