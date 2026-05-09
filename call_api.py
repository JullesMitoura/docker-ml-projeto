import requests

url = "http://localhost:8080"
endpoint = "/predict/day"
res = requests.post(f"{url}{endpoint}", json={"eficiencia": 90})

print(res.status_code)
response = res.json()

print(response["day"])