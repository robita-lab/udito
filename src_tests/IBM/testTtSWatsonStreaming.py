import os
<<<<<<< HEAD
import sounddevice as sd
import websocket
import json
import threading
import numpy as np
import base64
import pyaudio

CHUNK = 1024  # Tamaño de buffer optimizado
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Frecuencia compatible con Watson

print("test TtS Watson")
# Credenciales de IBM Watson
apikey=os.environ.get("WATSON_TTS_API_KEY", "")
#url = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/e82b66a7-1179-4249-8b60-4c7003432423"
#url = 'wss://api.us-south.text-to-speech.watson.cloud.ibm.com/v1/synthesize'
#wss://api.{location}.text-to-speech.watson.cloud.ibm.com/instances/{instance_id}/v1/synthesize
url = 'wss://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/e82b66a7-1179-4249-8b60-4c7003432423/v1/synthesize'

apikey_bytes = f"apikey:{apikey}".encode('ascii')
base64_bytes = base64.b64encode(apikey_bytes)
base64_string = base64_bytes.decode('ascii')
headers = {
    "Authorization": f"Basic {base64_string}"
}

# Texto a convertir en voz
text = "Hola, me llamo UDITO y soy un asistente virtual. Dime qué puedo hacer por ti"

print("open Audio Device")
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

def on_message(ws, message):
    stream.write(message)
# con sd
#    audio_data = np.frombuffer(message, dtype=np.int16)
#    sd.play(audio_data, samplerate=16000)
#    sd.wait()

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print(f"Conexión cerrada: {close_status_code} - {close_msg}")
    stream.stop_stream()
    stream.close()
    p.terminate()

def on_open(ws):
    def run():
        payload = {
            "text": text,
            "voice":'es-ES_LauraV3Voice',
            "accept":'audio/wav;rate=16000'
#            "accept": "audio/l16;rate=16000",
#            "voice": "es-ES_LauraV3Voice" #"es-ES_EnriqueV3Voice"
        }
        ws.send(json.dumps(payload))
    threading.Thread(target=run).start()


print("creando websocket")
ws = websocket.WebSocketApp(
    url,
    header=headers,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

print("running websocket")
# Iniciar la conexión
ws.run_forever()
=======
# TODO: Solamente funciona en inglés.

import sounddevice as sd
import websocket
import json
import threading
import numpy as np
import base64
import pyaudio

CHUNK = 1024  # Tamaño de buffer optimizado
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Frecuencia compatible con Watson

print("test TtS Watson")
# Credenciales de IBM Watson
apikey=os.environ.get("WATSON_TTS_API_KEY", "")
#url = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/e82b66a7-1179-4249-8b60-4c7003432423"
#url = 'wss://api.us-south.text-to-speech.watson.cloud.ibm.com/v1/synthesize'
#wss://api.{location}.text-to-speech.watson.cloud.ibm.com/instances/{instance_id}/v1/synthesize
url = 'wss://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/e82b66a7-1179-4249-8b60-4c7003432423/v1/synthesize'

apikey_bytes = f"apikey:{apikey}".encode('ascii')
base64_bytes = base64.b64encode(apikey_bytes)
base64_string = base64_bytes.decode('ascii')
headers = {
    "Authorization": f"Basic {base64_string}"
}

# Texto a convertir en voz
text = "Hola, me llamo UDITO y soy un asistente virtual. Dime qué puedo hacer por ti"

print("open Audio Device")
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

def on_message(ws, message):
    stream.write(message)
# con sd
#    audio_data = np.frombuffer(message, dtype=np.int16)
#    sd.play(audio_data, samplerate=16000)
#    sd.wait()

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print(f"Conexión cerrada: {close_status_code} - {close_msg}")
    stream.stop_stream()
    stream.close()
    p.terminate()

def on_open(ws):
    def run():
        payload = {
            "text": text,
            "voice":'es-ES_LauraV3Voice',
            "accept":'audio/wav;rate=16000'
#            "accept": "audio/l16;rate=16000",
#            "voice": "es-ES_LauraV3Voice" #"es-ES_EnriqueV3Voice"
        }
        ws.send(json.dumps(payload))
    threading.Thread(target=run).start()


print("creando websocket")
ws = websocket.WebSocketApp(
    url,
    header=headers,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

print("running websocket")
# Iniciar la conexión
ws.run_forever()
>>>>>>> f8ce2ec1ae480949a449280c2870e9cefa27901c
