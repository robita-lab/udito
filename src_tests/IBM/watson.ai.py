import requests
import json

url = "https://eu-de.ml.cloud.ibm.com"
#url = "https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/c867d38d-e863-403a-a256-30943d7ff9ec"
#api_key = "pQZgtA_rpSex91y4dbSx47HIeebITD9G782UFkxPbMnf"
api_key = "TP8qCL22zUpXkw2mHMtoAwJJZqM9ZBzKSwV_kPR60E0S"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model_id": "meta-llama/llama-3-3-70b-instruct",
#    "model_id": "ibm/granite-13b-chat-v2",  # o "mistralai/mixtral-8x7b-instruct-v0.1"
#    "model_id": "ibm/granite-3-8b-instruct",  # o "mistralai/mixtral-8x7b-instruct-v0.1"
    "input": "Explícame qué es la fotosíntesis en términos simples.",
    "parameters": {
        "decoding_method": "greedy",
        "max_new_tokens": 300,
        "min_new_tokens": 10
    }
}

response = requests.post(url, headers=headers, json=payload)
#print(json.dumps(response.json(), indent=2))
print(response)