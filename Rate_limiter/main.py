import requests

for i in range(11):
    r = requests.get("http://localhost:5000/api/data")
    print(f"{i+1}: {r.status_code} - {r.text}")
