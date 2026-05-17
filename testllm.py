import requests

payload = {
    "prompt":"Say hello",
    "max_tokens":100
}

response=requests.post(
    "http://localhost:8080/completion",
    json=payload
)

print(response.json())