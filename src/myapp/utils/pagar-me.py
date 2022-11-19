import requests

url = "https://api.pagar.me/core/v5/orders"

headers =  {
    'Authorization': 'Basic ' + 'sk_test_VLPbzRksWhyKZywx',
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers)

print(response.text)
