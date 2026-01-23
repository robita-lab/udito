# Dependencies:
#!pip install pyaudio
#!pip install sounddevice
#!pip install torch
#!pip install webrtcvad
#!pip install numpy

# Reconocedor de voz utilizando modelos_
# - VAD, modelo local
# - whisper modelo local para StT
# - IBM watson, modelo remoto

import sys 
from os.path import join, dirname
import usb.core
import usb.util
import time
import json
import io
import threading
import numpy as np
import queue
import pyaudio
import simpleaudio as sa
import wave
import webrtcvad
import whisper
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
sys.path.insert(0, '..')

from audio.Respeaker import RespeakerInterface
from audio.respeaker.usb_4_mic_array.tuning import Tuning

class StT:
    WATSON_API_KEY = "GcPMqCjN5je8m_Ef62KZNEm2xjnuyWaIEBtGuN-bFdvk"
    WATSON_URL = "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/09491bf9-4163-452c-9671-35a92c0ff521"
    FORMAT = pyaudio.paInt16  # Formato de audio
    WIDTH = 2
    CHANNELS = 1              # Audio mono
    RATE = 16000 #11025       # Frecuencia de muestreo compatible con Whisper
#    DURATION = 0.1 #0.03
    INPUT_DEVICE_ID = 4
    CHUNK = 1024 #DURATION * RATE  
    CHUNK = int(CHUNK)
    SILENCE_LIMIT = 0.8
    OUTPUT_WAV = "utterance.wav"
    RMS_THRES = 500
    MIN_UTTERANCE = 10

    def __init__(self, result_callback = None, user_speaking_callback = None):      
        print("StT::ctor")
        VAD_THRESHOLD = 90
        self.result_callback = result_callback
        self.user_speaking_callback = user_speaking_callback
        dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
        self.respeaker = Tuning(dev)

        try:
            self.respeaker.set_vad_threshold( VAD_THRESHOLD  )
        except:
            print("StT::Tuning device error. Trying dispose resource")
            usb.util.dispose_resources(dev)
            self.respeaker = Tuning(dev)
            self.respeaker.set_vad_threshold( VAD_THRESHOLD  )
            self.respeaker.write('AECFREEZEONOFF',0) # Adaptive Echo Canceler updates inhibit.'
            self.respeaker.write('ECHOONOFF',1) # Adaptive Echo Canceler updates inhibit.'
        self.audio = pyaudio.PyAudio()
        try:
            self.audio_queue = queue.Queue()
        except:
            print("StT::Error creando la audio_queue")
        self.print_audio_devices()
        self.audio_buffer = []
        self.user_speaking = False
        self.silence_counter = 0
        self.doa = None 
        self.stream = None

        try:
            self.stream = self.audio.open(
                format=self.audio.get_format_from_width(self.WIDTH), 
                channels=self.CHANNELS, 
                rate=self.RATE, 
                input=True, 
    #           output=False,
                input_device_index=self.INPUT_DEVICE_ID,
    #           output_device_index=OUTPUT_DEVICE_ID,
                frames_per_buffer=self.CHUNK, 
                stream_callback = self.callback)
        except:
            print("StT::ERROR opening audio stream")
            exit()

        # Crear el modelo de Whisper
        self.whisper = whisper.load_model("base")  # Cambiar el modelo según sea necesario
        # Inicializar VAD
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(2)  # Nivel de sensibilidad: 0 (menos sensible) a 3 (más sensible)
        self.watson = SpeechToTextV1(authenticator = IAMAuthenticator(self.WATSON_API_KEY))
        self.watson.set_service_url(self.WATSON_URL)
        self.model_id = 'es-ES_Multimedia'
        self.model = "watson" # "whisper"
        self.language_model_id = 0
        self.result = None
        self.text = None
        self.confidence = -1

    def start(self):
        self.stream.start_stream()
        self.active = True
        print("StT::🎤 Grabando (Ctrl+C para salir)...")
        threading.Thread(target=self.loop, daemon=True).start()

    def create_custom_model(self):
        self.language_model_id = self.watson.create_language_model(
            'es-ES_UDITO',
            'es-ES_Multimedia',
            description='Modelo con la palabra UDITO'
        ).get_result()

        self.watson.add_word(
            'self.language_model_id ',
            'UDITO',
            sounds_like=['udito'],
            display_as='UDITO'
        )

    def list_custom_models(self):
        language_models = self.watson.list_language_models().get_result()
        return language_models

    def train_custom_model(self, id):
        r = self.watson.train_language_model(customization_id = id, 
        word_type_to_add = "user",
        customization_weight = 0.4 # defaul 0.2 more gives importance to OOV
        )
        return r

    def upgrade_custom_model(self, id):
        r = self.watson.upgrade_custom_model(customization_id = id)
        return r

    def set_model(self, model):
        self.model_id = model

    def run(self):
        try:
            while self.stream.is_active():
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("StT::⏹️ Detenido por el usuario.")
        finally:
            self.close()

    def callback(self, in_data, frame_count, time_info, status):
        self.audio_queue.put(in_data)
        return (None, pyaudio.paContinue)

    # Función para detectar actividad de voz
    def is_speech(self, data):
    #    print("checking if is speech...")
        rms = np.sqrt(np.mean(np.square(data))) # ERROR: data is nan
#        print(rms)
        is_speech_rms = False
        is_speech_vad = False
        if rms > self.RMS_THRES:
            is_speech_rms = True
#        try:
#            is_speech_vad = self.vad.is_speech(data, self.RATE)
#        except:
#            print("StT::not possible to use VAD with data buffer")
        is_speech_respeaker = self.respeaker.is_voice() 
#        if is_speech_vad != is_speech_respeaker:
#            print("VAD says : ", is_speech_vad)
#            print("     but ReSpeaker says : ", is_speech_respeaker)
        is_speech = is_speech_vad | is_speech_respeaker

        return is_speech_respeaker

    # Función para reproducir audio
    def play_audio(self, data):
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True)
        self.stream.write(data)
        self.stream.stop_stream()
        self.stream.close()
    
    def play_buffer(self,frames):
        audio_bytes = b''.join(frames)
        play_obj = sa.play_buffer(audio_bytes, num_channels=1, bytes_per_sample=2, sample_rate=self.RATE)
        play_obj.wait_done()

    def print_audio_devices(self):
        print("StT::Dispositivos de audio disponibles:")
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            print(f"ID: {i}, Nombre: {info['name']}, Entrada: {info['maxInputChannels']}, Salida: {info['maxOutputChannels']}")

    def loop(self):
        print("StT::loop 🎙️ Esperando voz...")
        silence_counter = 0
        self.user_speaking = False

        while self.active:
            data = self.audio_queue.get()
            samples = np.frombuffer(data, dtype = np.int16)
            if self.is_speech(samples):
                if not self.user_speaking:
                    print("StT::🎤 Usuario comenzo a hablar...")
                    frames = []
                    self.doa = self.respeaker.direction
                    print("angle",self.doa)
                    self.user_speaking = True
                    if self.user_speaking_callback is not None:
                        self.user_speaking_callback(True)
                silence_counter = 0
                frames.append(data)
            else:
                if self.user_speaking:
                    frames.append(data)
                    silence_counter += self.CHUNK / self.RATE
                    print(silence_counter)
                    if silence_counter > self.SILENCE_LIMIT:
                        if len(frames) > self.MIN_UTTERANCE:
                            print("StT::🛑...end of utterance")
                            self.user_speaking = False
                            if self.user_speaking_callback is not None:
                                self.user_speaking_callback(False)
                            print("StT::Transcribiendo")
#                            self.play_buffer(frames)
                            self.recoginze_buffer(frames)
                            self.save_wav_from_buffer(frames)
                            self.result_callback(self.result)
                        else:
                            print("StT::🎧 Ruido corto ignorado.")
                        frames = []
                        silence_counter = 0

    def recoginze_buffer(self, frames):
        audio_bytes = b''.join(frames)
        audio_stream = io.BytesIO(audio_bytes)
        try:
            self.result = self.watson.recognize(
                audio=audio_stream,
                content_type='audio/l16;rate=16000;channels=1',
                model=self.model_id, #es-ES, es-ES_BroadbandModel, es-ES_NarrowbandModel, es-ES_Multimedia, es-ES_Telephony, 
#                language_customization_id = self.customization_id,
                smart_formatting=True,
                timestamps=True,
                word_confidence=True,
#                keywords=['UDITO'],        #previous generation
#                keywords_threshold=0.5     #previous generation
#                speech_detection_sensitivity = 0.5,
                low_latency = True             #next-generation models Multimedia/Telephony
#               character_instertion_bias       #next-generation models Multimedia/Telephony

            ).get_result()
            if self.result.get('results'):
                self.text = self.result['results'][0]['alternatives'][0]['transcript'].strip()
                self.confidence = self.result['results'][0]['alternatives'][0]['confidence']
                return self.result
            else:
                return None
        except Exception as e:
            print("StT::⚠️ Error en reconocimiento:", e)
            return None
#        except ApiException as ex:
#            print "Method failed with status code " + str(ex.code) + ": " + ex.message



# ERROR: toma el audio con cortes
    def loop_old(self, name):
        print("Esperando actividad de voz... ")
        while self.active:
            data = self.stream.read(self.CHUNK, exception_on_overflow = False)
            if self.is_speech(data):
                if not self.user_speaking:
                    print("🎤 Usuario comenzo a hablar...")
                    self.doa = self.respeaker.direction
                    print("angle",self.doa)
                    self.audio_buffer = []
                    self.user_speaking = True
                    self.silence_counter = 0
                self.audio_buffer.append(data)
            else:
                if self.user_speaking:
                    self.silence_counter += self.CHUNK / self.RATE
                    if self.silence_counter > self.SILENCE_LIMIT:
                        print("🛑...end of utterance")
                        self.user_speaking = False
                        self.silence_counter = 0
                        print("Transcribiendo")
                        self.save_wave()
                        self.result = self.recognize()
                        self.result_callback(self.result)  
            self.result =  None     
        self.close()
        
    def save_wav_from_buffer(self, frames):
        audio_bytes = b"".join(frames)

        with wave.open(self.OUTPUT_WAV, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)       # int16 → 2 bytes
            wf.setframerate(16000)
            wf.writeframes(audio_bytes)

        print(f"💾 Guardado WAV: {self.OUTPUT_WAV}")


    def save_wave(self):
        wf = wave.open(self.OUTPUT_WAV, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.audio_buffer))
        wf.close()
        print(f"💾 Audio guardado en {self.OUTPUT_WAV}")

    def recognize(self):
        if self.model == "watson":
            with open(self.OUTPUT_WAV, 'rb') as audio_file:
                self.result = self.watson.recognize(
                    audio=audio_file,
                    content_type='audio/wav',
                    model=self.model_id,  # puedes cambiar por 'es-ES_BroadbandModel'
                    timestamps=True,
                    word_confidence=True
                ).get_result()
                print(self.result)
            if self.result.get('results'):
                self.text = self.result['results'][0]['alternatives'][0]['transcript'].strip()
                self.confidence = self.result['results'][0]['alternatives'][0]['confidence']
#                print(f"🗣️ Transcripción: {self.text}")
#                print(f"🗣️ Confidence: {self.confidence}")
            else:
                self.result = None
        elif self.model == "whisper":
            audio_np = np.frombuffer(self.audio_buffer, dtype=np.int16).astype(np.float32) / 32768.0
            self.result = self.whisper.transcribe(audio_np, language="es")            
        return self.result

    def close(self):
        self.active = False
        self.respeaker.close()
        try:
            self.stream.stop_stream()
            self.stream.close()
        except:
            print("StT::no stream found...")
        self.audio.terminate()

    def __del__(self):
        print("StT::dtor")
        self.close()