from TTS.api import TTS
import sounddevice as sd
import pyaudio
import numpy as np


p = pyaudio.PyAudio()
#for i in range(p.get_device_count()):
#    print(i,p.get_device_info_by_index(i)["defaultSampleFormat"])

# Descarga y usa el modelo en español
tts = TTS(model_name="tts_models/es/css10/vits")

# Genera el audio en español
tts.tts_to_file(
    text="Hola, estoy muy feliz de hablar contigo.",
    file_path="output.wav"
)

print("¡Archivo de audio generado con éxito!")

audio = tts.tts("Hola, estoy muy feliz de hablar contigo.")
audio_np = np.asarray(audio)
print(type(audio), len(audio))
print("shape: ", audio_np.shape)
print("first element: ", type(audio[0]))
sd.play(audio, samplerate=22050)
sd.wait()