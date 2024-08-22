import requests

url = "https://api.vapi.ai/assistant/e79c0ebf-63b5-49b3-899f-7fea95a631d2"

payload = {
    "serverUrl": "https://hook.us1.make.com/qt11rrxb3v5l2ffebywvod8brwu0pioo",
	"serverMessages": [
    "end-of-call-report"
  ]
}

headers = {
    "Authorization": "Bearer ",
    "Content-Type": "application/json"
}

response = requests.request("PATCH", url, json=payload, headers=headers)

print(response.text)