import requests

url = "https://api.vapi.ai/assistant/951bb5a8-162d-4ffb-9673-a6990e2929fd"

payload = {
  "voice": {
		"speed": 0.9,
		"voiceId": "melissa",
		"provider": "playht",
		"fillerInjectionEnabled": False
	},
	"recordingEnabled": False,
	"endCallFunctionEnabled": True,
	"firstMessageMode":"assistant-speaks-first-with-model-generated-message",
	"model": {
		"url": "https://4476-136-158-25-179.ngrok-free.app/api",
		"model": "dmapi",
		"provider": "custom-llm"
	},
	"transcriber": {
		"model": "nova-2",
		"language": "en",
		"provider": "deepgram"
	},
	"silenceTimeoutSeconds": 25,
	"clientMessages": [
		"transcript",
		"hang",
		"function-call",
		"speech-update",
		"metadata",
		"conversation-update"
	],
	"serverMessages": [
		"end-of-call-report",
		"status-update",
		"hang",
		"function-call"
	],
	"backgroundSound": "office"
}

headers = {
    "Authorization": "Bearer 48d98dd9-e7d5-40a3-a3bc-643c32dc570d",
    "Content-Type": "application/json"
}

response = requests.request("PATCH", url, json=payload, headers=headers)

print(response.text)