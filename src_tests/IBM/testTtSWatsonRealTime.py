import os
<<<<<<< HEAD
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyaudio

print("test TtS Watson")
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6 # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 4  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Configuración de autenticación
api_key = os.environ.get("WATSON_TTS_API_KEY", "")
url = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/e82b66a7-1179-4249-8b60-4c7003432423"
print("connecting...")
authenticator = IAMAuthenticator(api_key)
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(url)
print("OK!")

texto = "Hola, me llamo UDITO. Dime qué puedo hacer por ti"

print("Sending text to Watson...")

response = text_to_speech.synthesize(
    texto,
    voice='es-ES_LauraV3Voice',
    accept='audio/wav;rate=16000'#'audio/wav'
).get_result()

print("Playing audio...")
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RESPEAKER_RATE,#22050,
                output=True,
                output_device_index=RESPEAKER_INDEX)

stream.write(response.content)
stream.stop_stream()
stream.close()
p.terminate()
=======
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyaudio
import sounddevice as sd
import requests
import io
from pydub import AudioSegment

def stream_audio(url):
    response = requests.get(url, stream=True)
    audio = AudioSegment.from_file(io.BytesIO(response.content))
    sd.play(audio.get_array_of_samples(), samplerate=16000)
    sd.wait()

# Prueba de reproducción
stream_audio('https://api.example.com/audio-stream')

print("test TtS Watson")
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6 # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
# run getDeviceInfo.py to get index
RESPEAKER_INDEX = 4  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Configuración de autenticación
api_key = os.environ.get("WATSON_TTS_API_KEY", "")
url = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/e82b66a7-1179-4249-8b60-4c7003432423"
print("connecting...")
authenticator = IAMAuthenticator(api_key)
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(url)
print("OK!")

texto = "Hola, me llamo UDITO. Dime qué puedo hacer por ti"

print("Sending text to Watson...")

response = text_to_speech.synthesize(
    texto,
    voice='es-ES_LauraV3Voice',
    accept='audio/wav;rate=16000'#'audio/wav'
).get_result()

print("Playing audio...")


# Con pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RESPEAKER_RATE,#22050,
                output=True,
                output_device_index=RESPEAKER_INDEX)

stream.write(response.content)
stream.stop_stream()
stream.close()
p.terminate()
>>>>>>> f8ce2ec1ae480949a449280c2870e9cefa27901c
