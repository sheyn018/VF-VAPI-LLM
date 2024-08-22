import requests

url = "https://api.vapi.ai/analytics"

payload = {"queries": [
        {
            "table": "call",
            "name": "e79c0ebf-63b5-49b3-899f-7fea95a631d2",
            "operations": [
                {
                    "operation": "count",
                    "column": "id"
                },
                {
                    "operation": "avg",
                    "column": "cost"
                },
                {
                    "operation": "avg",
                    "column": "duration"
                }
            ],
            "timeRange": {
                "step": "month",
                "start": "2024-07-16T05:31:56Z",
                "end": "2024-07-17T05:31:56Z"
            }
        }
    ]}
headers = {
    "Authorization": "Bearer 79087b31-e0cd-4023-8f7d-a4518453c1e7",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)