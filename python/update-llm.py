import requests

url = "https://api.vapi.ai/assistant/793a6374-4755-4d0b-bb49-99cef3f9be6e"

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
		"url": "https://992d-136-158-25-179.ngrok-free.app/api",
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
    "Authorization": "Bearer ",
    "Content-Type": "application/json"
}

response = requests.request("PATCH", url, json=payload, headers=headers)

print(response.text)