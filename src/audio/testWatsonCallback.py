import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

import pyaudio
import requests
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Configurar IBM Watson TTS
API_KEY = os.environ.get("WATSON_TTS_API_KEY", "")
URL = os.environ.get("WATSON_TTS_URL", "")

authenticator = IAMAuthenticator(API_KEY)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(URL)

# Texto a convertir en voz
text = "Hola, este es un ejemplo de síntesis de voz en tiempo real."

# Solicitar audio en formato PCM lineal de 16 bits (audio/l16;rate=16000)
response = tts.synthesize(
    text,
    voice="es-LA_SofiaV3Voice",  # Puedes cambiar la voz según disponibilidad
    accept="audio/l16;rate=16000"
).get_result()

# Leer el audio en chunks
audio_stream = response.content

# Configurar PyAudio en modo callback
p = pyaudio.PyAudio()

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6 # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 4  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Convertir audio en iterador de chunks
def audio_generator():
    for i in range(0, len(audio_stream), CHUNK):
        yield audio_stream[i:i + CHUNK]

audio_iter = audio_generator()

# Callback de PyAudio
def callback(in_data, frame_count, time_info, status):
    try:
        data = next(audio_iter)
    except StopIteration:
        return (None, pyaudio.paComplete)
    return (data, pyaudio.paContinue)

# Abrir stream de audio
#stream = p.open(format=FORMAT,
#                channels=CHANNELS,
#                rate=RATE,
#                output=True,
#                stream_callback=callback)
stream = p.open(format=pyaudio.paInt16,
            channels=1,
            rate=RESPEAKER_RATE,
            output=True,
            output_device_index=RESPEAKER_INDEX,
            frames_per_buffer=CHUNK,
            stream_callback=callback)
stream.start_stream()

# Esperar a que termine la reproducción
while stream.is_active():
    pass

# Cerrar PyAudio
stream.stop_stream()
stream.close()
p.terminate()

import pyaudio
import requests
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Configurar IBM Watson TTS
API_KEY = os.environ.get("WATSON_TTS_API_KEY", "")
URL = os.environ.get("WATSON_TTS_URL", "")

authenticator = IAMAuthenticator(API_KEY)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(URL)

# Texto a convertir en voz
text = "Hola, este es un ejemplo de síntesis de voz en tiempo real."

# Solicitar audio en formato PCM lineal de 16 bits (audio/l16;rate=16000)
response = tts.synthesize(
    text,
    voice="es-LA_SofiaV3Voice",  # Puedes cambiar la voz según disponibilidad
    accept="audio/l16;rate=16000"
).get_result()

# Leer el audio en chunks
audio_stream = response.content

# Configurar PyAudio en modo callback
p = pyaudio.PyAudio()

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6 # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 4  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Convertir audio en iterador de chunks
def audio_generator():
    for i in range(0, len(audio_stream), CHUNK):
        yield audio_stream[i:i + CHUNK]

audio_iter = audio_generator()

# Callback de PyAudio
def callback(in_data, frame_count, time_info, status):
    try:
        data = next(audio_iter)
    except StopIteration:
        return (None, pyaudio.paComplete)
    return (data, pyaudio.paContinue)

# Abrir stream de audio
#stream = p.open(format=FORMAT,
#                channels=CHANNELS,
#                rate=RATE,
#                output=True,
#                stream_callback=callback)
stream = p.open(format=pyaudio.paInt16,
            channels=1,
            rate=RESPEAKER_RATE,
            output=True,
            output_device_index=RESPEAKER_INDEX,
            frames_per_buffer=CHUNK,
            stream_callback=callback)
stream.start_stream()

# Esperar a que termine la reproducción
while stream.is_active():
    pass

# Cerrar PyAudio
stream.stop_stream()
stream.close()
p.terminate()
