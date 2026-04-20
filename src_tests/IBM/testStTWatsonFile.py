import os
from os.path import join, dirname
import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

apikey = os.environ.get("WATSON_STT_API_KEY", "")
url = "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521"

authenticator = IAMAuthenticator(apikey)
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url(url)

#speech_models = speech_to_text.list_models().get_result()
#print(json.dumps(speech_models, indent=2))

speech_model = speech_to_text.get_model('es-ES').get_result()
print(json.dumps(speech_model, indent=2))


with open(join(dirname(__file__), '../.', 'testSpeech.wav'),
               'rb') as audio_file:
    speech_recognition_results = speech_to_text.recognize(
        model = 'es-ES_Multimedia', #'es-ES_Telephony',#0.92 #'es-ES_Multimedia', #0.98 # 'es-ES_NarrowbandModel',#0.94 #'es-ES_BroadbandModel', # 0.95 # 'es-ES', # 0.85
        audio=audio_file,
        content_type='audio/wav'
#        word_alternatives_threshold=0.9,
#        keywords=['texto', 'prueba', 'hola'],
#        keywords_threshold=0.5
    ).get_result()
print(json.dumps(speech_recognition_results, indent=2))

#es-AR_BroadbandModel,es-AR_NarrowbandModel,es-CL_BroadbandModel,es-CL_NarrowbandModel,es-CO_BroadbandModel,es-CO_NarrowbandModel,es-LA_Telephony,es-MX_BroadbandModel,es-MX_NarrowbandModel,es-PE_BroadbandModel,es-PE_NarrowbandModel,
# es-ES_BroadbandModel,
# es-ES_NarrowbandModel,
# es-ES_Multimedia,
# es-ES_Telephony,

# {
#      "name": "es-ES_Multimedia",
#      "rate": 16000,
#      "language": "es-ES",
#      "description": "Castilian Spanish multimedia model for broadband audio (16kHz)",
#   #   "supported_features": {
#   #     "custom_acoustic_model": false,
#   #     "custom_language_model": true,
#   #     "low_latency": true,
#   #     "speaker_labels": true
#   #   }
#
    #  "name": "es-LA_Telephony",
    #  "rate": 8000,
    #  "language": "es-LA",
    #  "description": "Latin American Spanish telephony model for narrowband audio (8kHz)",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": true,
    #    "speaker_labels": true
    #  }
#
    #    {
    #  "name": "es-AR",
    #  "rate": 8000,
    #  "language": "es-AR",
    #  "description": "Large Argentinian Spanish Model",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": false,
    #    "speaker_labels": true
    #  }
#
    #   {
    #  "name": "es-ES_Telephony",
    #  "rate": 8000,
    #  "language": "es-ES",
    #  "description": "Castilian Spanish telephony model for narrowband audio (8kHz)",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": true,
    #    "speaker_labels": true
    #  },
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-ES_Telephony"
    #}
#
    #    {
    #  "name": "es-PE",
    #  "rate": 8000,
    #  "language": "es-PE",
    #  "description": "Large Peruvian Spanish Model",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": false,
    #    "speaker_labels": true
    #  },
    #  "decoder_method": "decode_ctc_v2_0_0",
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-PE"
    #}
#
    #    {
    #  "name": "es-MX",
    #  "rate": 8000,
    #  "language": "es-MX",
    #  "description": "Large Mexican Spanish Model",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": false,
    #    "speaker_labels": true
    #  },
    #  "decoder_method": "decode_ctc_v2_0_0",
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-MX"
    #}
#
    #    {
    #  "name": "es-CO",
    #  "rate": 8000,
    #  "language": "es-CO",
    #  "description": "Large Colombian Spanish Model",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": false,
    #    "speaker_labels": true
    #  },
    #  "decoder_method": "decode_ctc_v2_0_0",
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-CO"
    #}
#
    #    {
    #  "name": "es-AR",
    #  "rate": 8000,
    #  "language": "es-AR",
    #  "description": "Large Argentinian Spanish Model",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": false,
    #    "speaker_labels": true
    #  },
    #  "decoder_method": "decode_ctc_v2_0_0",
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-AR"
    #},
    #  {
    #  "name": "es-ES_Telephony",
    #  "rate": 8000,
    #  "language": "es-ES",
    #  "description": "Castilian Spanish telephony model for narrowband audio (8kHz)",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": true,
    #    "speaker_labels": true
    #  },
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-ES_Telephony"
    #}
#
    #    {
    #  "name": "es-PE",
    #  "rate": 8000,
    #  "language": "es-PE",
    #  "description": "Large Peruvian Spanish Model",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": false,
    #    "speaker_labels": true
    #  },
    #  "decoder_method": "decode_ctc_v2_0_0",
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-PE"
    #},
#
    #   {
    #  "name": "es-MX",
    #  "rate": 8000,
    #  "language": "es-MX",
    #  "description": "Large Mexican Spanish Model",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": false,
    #    "speaker_labels": true
    #  },
    #  "decoder_method": "decode_ctc_v2_0_0",
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-MX"
    #},
#
    #   {
    #  "name": "es-CO",
    #  "rate": 8000,
    #  "language": "es-CO",
    #  "description": "Large Colombian Spanish Model",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": false,
    #    "speaker_labels": true
    #  },
    #  "decoder_method": "decode_ctc_v2_0_0",
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-CO"
    #}
#
    #   {
    #  "name": "es-ES",
    #  "rate": 8000,
    #  "language": "es-ES",
    #  "description": "Large Castilian Spanish Model",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": false,
    #    "speaker_labels": true
    #  },
    #  "decoder_method": "decode_ctc_v2_0_0",
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-ES"
    #},
    #    {
    #  "name": "es-CL",
    #  "rate": 8000,
    #  "language": "es-CL",
    #  "description": "Large Chilean Spanish Model",
    #  "supported_features": {
    #    "custom_acoustic_model": false,
    #    "custom_language_model": true,
    #    "low_latency": false,
    #    "speaker_labels": true
    #  },
    #  "decoder_method": "decode_ctc_v2_0_0",
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-CL"
    #},
#
    #   {
    #  "name": "es-CO_NarrowbandModel",
    #  "rate": 8000,
    #  "language": "es-CO",
    #  "description": "Colombian Spanish narrowband model.",
    #  "supported_features": {
    #    "custom_acoustic_model": true,
    #    "custom_language_model": true,
    #    "speaker_labels": true
    #  },
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-CO_NarrowbandModel"
    #},
#
    #    {
    #  "name": "es-PE_NarrowbandModel",
    #  "rate": 8000,
    #  "language": "es-PE",
    #  "description": "Peruvian Spanish narrowband model.",
    #  "supported_features": {
    #    "custom_acoustic_model": true,
    #    "custom_language_model": true,
    #    "speaker_labels": true
    #  },
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-PE_NarrowbandModel"
    #},
    #    {
    #  "name": "es-PE_BroadbandModel",
    #  "rate": 16000,
    #  "language": "es-PE",
    #  "description": "Peruvian Spanish broadband model.",
    #  "supported_features": {
    #    "custom_acoustic_model": true,
    #    "custom_language_model": true,
    #    "speaker_labels": true
    #  },
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-PE_BroadbandModel"
    #},
    #   {
    #  "name": "es-CL_BroadbandModel",
    #  "rate": 16000,
    #  "language": "es-CL",
    #  "description": "Chilean Spanish broadband model.",
    #  "supported_features": {
    #    "custom_acoustic_model": true,
    #    "custom_language_model": true,
    #    "speaker_labels": true
    #  },
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-CL_BroadbandModel"
    #}
#
    #    {
    #  "name": "es-CL_NarrowbandModel",
    #  "rate": 8000,
    #  "language": "es-CL",
    #  "description": "Chilean Spanish narrowband model.",
    #  "supported_features": {
    #    "custom_acoustic_model": true,
    #    "custom_language_model": true,
    #    "speaker_labels": true
    #  },
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-CL_NarrowbandModel"
    #}
#
    #  {
    #  "name": "es-MX_NarrowbandModel",
    #  "rate": 8000,
    #  "language": "es-MX",
    #  "description": "Mexican Spanish narrowband model.",
    #  "supported_features": {
    #    "custom_acoustic_model": true,
    #    "custom_language_model": true,
    #    "speaker_labels": true
    #  },
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-MX_NarrowbandModel"
    #},
#
    #    {
    #  "name": "es-ES_NarrowbandModel",
    #  "rate": 8000,
    #  "language": "es-ES",
    #  "description": "Castilian Spanish narrowband model.",
    #  "supported_features": {
    #    "custom_acoustic_model": true,
    #    "custom_language_model": true,
    #    "speaker_labels": true
    #  },
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-ES_NarrowbandModel"
    #},
#
    #   {
    #  "name": "es-ES_BroadbandModel",
    #  "rate": 16000,
    #  "language": "es-ES",
    #  "description": "Castilian Spanish broadband model.",
    #  "supported_features": {
    #    "custom_acoustic_model": true,
    #    "custom_language_model": true,
    #    "speaker_labels": true
    #  },
    #  "url": "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521/v1/models/es-ES_BroadbandModel"
    #}