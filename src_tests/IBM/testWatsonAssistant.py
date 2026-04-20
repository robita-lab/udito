import os
import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey=os.environ.get("WATSON_ASSISTANT_API_KEY", "")
url = "https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/c867d38d-e863-403a-a256-30943d7ff9ec"



assistant_id = "a8178f33-219f-47b5-85a3-d882ea7b7b6d"
environment_id = assistant_id
action_skill_id = "715211b2-be5b-47c4-a141-9d11b5b35aa8"
draft_environment_id = "6fa48dd4-f664-4e00-8fac-ed67338ab89c"
live_environment_id = "7c612a5d-3c1e-4eff-a0d3-a8778fa02386"


authenticator = IAMAuthenticator(apikey)

assistant = AssistantV2(
    version='2024-08-25',
    authenticator=authenticator)
assistant.set_service_url('https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/c867d38d-e863-403a-a256-30943d7ff9ec')

response = assistant.create_session(
    assistant_id=draft_environment_id #environment_id
).get_result()
print(json.dumps(response, indent=2))
session_id = response["session_id"]

#assistant.set_disable_ssl_verification(True)
assistant.set_http_config({'timeout': 100})


response = assistant.message(
    assistant_id=draft_environment_id, #environment_id
    environment_id=draft_environment_id,
    session_id="e618e32a-d56f-4243-818a-f9f804df3e42",
    input={
        'message_type': 'text',
        'text': 'Hola'
    }
).get_result()

print(json.dumps(response, indent=2))
