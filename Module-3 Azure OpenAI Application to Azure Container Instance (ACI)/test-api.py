import requests

response = requests.post(
    "http://myappdemo123unique.centralindia.azurecontainer.io:8000/ask",
    json={"question": "What is Azure?"}
)

print(response.json())