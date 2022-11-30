import requests

url = 'https://us-central1-sonorous-sign-345710.cloudfunctions.net/img-classifier'

data = {'url': 'http://bit.ly/mlbookcamp-pants'}

result = requests.post(url, json=data).json()
print(result)