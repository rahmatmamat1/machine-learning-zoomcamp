import requests

url = 'http://localhost:9696/'
# url = 'https://fraud-service-i2gw4npszq-uw.a.run.app'

click = {
    "ip": 23155,
    "app": 5,
    "device": 1,
    "os": 30,
    "channel": 20,
    "day": 7,
    "hour": 6,
    "minute": 20,
    "second": 15
}

response = requests.post(url, headers={'Content-Type': 'application/json'}, json=click).json()

print(response)