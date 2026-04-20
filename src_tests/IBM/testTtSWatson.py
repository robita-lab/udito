import os
# see ibm.github watsonx-ai-python
# pip install ibm-watson
# pip install ibm-watson-ai

import json
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey=os.environ.get("WATSON_TTS_API_KEY", "")
url = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/e82b66a7-1179-4249-8b60-4c7003432423"
authenticator = IAMAuthenticator(apikey)

text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url(url)

#voices = text_to_speech.list_voices().get_result()
#print(json.dumps(voices, indent=2))

#custom_models = text_to_speech.list_custom_models().get_result() # not lite plan, yes paid plan
#print(json.dumps(custom_models, indent=2))

#speakers = text_to_speech.list_speaker_models().get_result()
#print(json.dumps(speakers, indent=2))
with open('es-ES_LauraV3Voice_-20+50.wav', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            'Hola, me llamo UDITO. Dime qué puedo hacer por ti',
            voice='es-ES_LauraV3Voice',#es-ES_LauraV3Voice', #'es-ES_EnriqueVoice',es-ES_EnriqueV3Voice,es-ES_LauraV3Voice,es-LA_SofiaV3Voice,es-US_SofiaV3Voice
            accept='audio/wav',rate_percentage=20,pitch_percentage=50        
        ).get_result().content)
#speakers = text_to_speech.list_speaker_models().get_result()
#print(json.dumps(speakers, indent=2))

#with open('es-ES_LauraV3Voice_-20+50.wav', 'wb') as audio_file:
#    audio_file.write(
#        text_to_speech.synthesize(
#            'Hola, esto es un texto de prueba',
#            voice='es-ES_LauraV3Voice',#es-ES_LauraV3Voice', #'es-ES_EnriqueVoice',es-ES_EnriqueV3Voice,es-ES_LauraV3Voice,es-LA_SofiaV3Voice,es-US_SofiaV3Voice
#            accept='audio/wav',rate_percentage=20,pitch_percentage=50        
#        ).get_result().content)
