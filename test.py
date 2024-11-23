import requests

response = requests.post(
    "http://localhost:8000/summarize",
    json={"url": "https://www.youtube.com/watch?v=pMX2cQdPubk&ab_channel=MarquesBrownlee"}
)
print(response.json())