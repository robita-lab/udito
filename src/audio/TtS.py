# requirementes TTS (CoquiTTS)
# también hace TtS mediante voces de IBM-Watson
import os
from TTS.api import TTS
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pydub import AudioSegment
import requests
import io
import pyaudio
import sounddevice as sd
import numpy as np
import websocket
import json
import threading
import queue
import base64
import time
import re

RESPEAKER_RATE = 22050 #16000 #coqui 22050, watson 16000
RESPEAKER_CHANNELS = 6 # change base on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 4  # refer to input device id
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

# Configuración de autenticación
api_key = "wFGvz40iMm2kOmhvIAd3TpNcwUcgL8gfrK9agNb9K_TY"
url = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/e82b66a7-1179-4249-8b60-4c7003432423"
print("connecting...")
authenticator = IAMAuthenticator(api_key)

class TtS( threading.Thread ):
    def __init__(self, robot_speaking_callback = None):
        print("TtS::ctor")
        super().__init__()
        self.robot_speaking_callback = robot_speaking_callback
        self.model = "tts_models/es/css10/vits" # 500ms de latencia # da NNPACK! error
#        self.model = "tts_models/multilingual/multi-dataset/xtts_v2" # 8 segundos de latencia
#        self.model = "tts_models/multilingual/multi-dataset/xtts_v1.1" #OSError: [WinError 6] Controlador no válido
                                    # UBUNTU: error raro de pytorch 
#        self.model = "tts_models/es/mai/tacotron2-DDC"
#        self.model = "tts_models/spa/fairseq/vits" # 
        self.emotion = "neutral"
        self.coqui_speakers_idx = ['Claribel Dervla', 'Daisy Studious', 'Gracie Wise', 'Tammie Ema', 'Alison Dietlinde', 'Ana Florence', 'Annmarie Nele', 'Asya Anara', 'Brenda Stern', 'Gitta Nikolina', 'Henriette Usha', 'Sofia Hellen', 'Tammy Grit', 'Tanja Adelina', 'Vjollca Johnnie', 'Andrew Chipper', 'Badr Odhiambo', 'Dionisio Schuyler', 'Royston Min', 'Viktor Eka', 'Abrahan Mack', 'Adde Michal', 'Baldur Sanjin', 'Craig Gutsy', 'Damien Black', 'Gilberto Mathias', 'Ilkin Urbano', 'Kazuhiko Atallah', 'Ludvig Milivoj', 'Suad Qasim', 'Torcull Diarmuid', 'Viktor Menelaos', 'Zacharie Aimilios', 'Nova Hogarth', 'Maja Ruoho', 'Uta Obando', 'Lidiya Szekeres', 'Chandra MacFarland', 'Szofi Granger', 'Camilla Holmström', 'Lilya Stainthorpe', 'Zofija Kendrick', 'Narelle Moon', 'Barbora MacLean', 'Alexandra Hisakawa', 'Alma María', 'Rosemary Okafor', 'Ige Behringer', 'Filip Traverse', 'Damjan Chapman', 'Wulf Carlevaro', 'Aaron Dreschner', 'Kumar Dahl', 'Eugenio Mataracı', 'Ferran Simen', 'Xavier Hayasaka', 'Luis Moray', 'Marcos Rudaski']
        self.coqui_speaker = "Andrew Chipper"

        self.watson_speakers_idx =['es-ES_LauraV3Voice', 
                                    'es-ES_EnriqueVoice', 
                                    'es-ES_EnriqueV3Voice', 
                                    'es-LA_SofiaV3Voice', 
                                    'es-US_SofiaV3Voice']
        self.watson_speaker = "es-ES_LauraV3Voice"
        self.tts_model = TTS(model_name=self.model)
#        self.tts_model = None   # Para acelerar el arrancque no carga el modelo local
        self.coqui_rate = self.tts_model.synthesizer.output_sample_rate

        self.tts_watson = TextToSpeechV1(authenticator=authenticator)
        self.tts_watson.set_service_url(url) 

        self.p = pyaudio.PyAudio()
        self.audio_device = self.p.open(format=pyaudio.paInt16,
                channels=1,
                rate=self.coqui_rate, #RESPEAKER_RATE,
                output=True)
#                output_device_index=RESPEAKER_INDEX)
        self.audio_device_type = "pyaudio" # "sounddevice"
#        self.tts_engine = "watson" # "coquitts"
        self.tts_engine = "coquitts"
        self.text = None
        self.text_queue = queue.Queue()
        self.ad = None
        self.paused = threading.Event()
        self.paused.clear()
        self.stop_event = threading.Event()
        self.start_event = threading.Event()
        self.done_event = threading.Event()
        self.lock = threading.Lock()
        self.is_speaking = False
        self.audio_device.start_stream()
        self.start()

    def set_tts_audio_device(self, engine):
        self.audio_device_type = engine

    def set_tts_coqui_speaker(self, id):
        self.speaker = self.coqui_speakers_idx[id]
        self.tts_engine = "coquitts"

    def set_tts_watson_speaker(self, id):
        self.speaker = self.watson_speakers_idx[id]
        self.tts_engine = "watson"

    def set_tts_speaker(self, speaker):
        self.speaker = speaker
        if speaker in self.coqui_speakers_idx:
            self.tts_engine = "coquitts"
        elif speaker in self.watson_speakers_idx:
            self.tts_engine = "watson"

    def tts_to_file_coqui(self, text):
        self.tts_model.tts_to_file(text=text, file_path=WAVE_OUTPUT_FILENAME)

    def tts_to_file_watson(self, text):
        response = self.tts_watson.synthesize(
            text,
            voice=self.watson_speaker,
            accept='audio/wav;rate=16000'#'audio/wav'
        ).get_result()
        audio_data = response.content
        with open(WAVE_OUTPUT_FILENAME, 'wb') as audio_file:
            audio_file.write(audio_data)

    def speak(self, text):
#        with self.lock:
            if text == "":
                print("No text to speak")
                self.text = None
                return
            for utt in re.split(r'(?<=[.!?])\s+', text):
                self.text_queue.put(utt) 
            print("TtS::speak, text queue has %d utterances" %(self.text_queue.qsize()))
     #       self.paused.clear()

    def tts(self, text):
        self.ad = self.get_audio_data(text)
        self.is_speaking = True
        if self.robot_speaking_callback is not None:
            self.robot_speaking_callback(True)
        self.write_audio_data(self.ad)
        self.is_speaking = False
        if self.robot_speaking_callback is not None:
            self.robot_speaking_callback(False)

    def activate(self):
        self.done_event.clear()
        self.start_event.set()
    
    def wait_until_done(self):
        self.done_event.wait()

    def tick(self):
        self.activate()
        self.wait_until_done()

    # TODO: Hacer una cola de audio_data por frases y abrir un hilo de write_audio
    # para ir generando audio_data, mientras se sintetiza
    def run(self):
        while not self.stop_event.is_set():
            self.start_event.wait()
            while not self.text_queue.empty():
#                with self.lock:
                    text = self.text_queue.get()
#                    print("TtS: %s " %(text))
                    self.tts(text)
                    if self.paused.is_set(): 
                        clear_queue(self.text_queue)
                        break
                    self.text_queue.task_done()
#                print("TtS::speak, text queue has %d utterances" %(len(self.text_queue)))
            self.paused.clear()    
            self.done_event.set()
            self.start_event.clear()

    def get_audio_data(self,text):
        if len(text) <= 0 :
            return None
        audio_data = None
        if(self.tts_engine == "watson"):
            response = self.tts_watson.synthesize(
                text,
                voice=self.watson_speaker,
                accept='audio/l16;rate=16000'#'audio/wav'
            ).get_result()
            audio_data = response.content
        elif(self.tts_engine == "coquitts"):
            audio = self.tts_model.tts(text) 
#                              emotion=self.emotion, 
#                              language="es", 
#                              speaker=self.coqui_speaker) # comment if model is not multi-speaker
#            audio_int = (audio * 32767).astype(np.int16)
            audio = np.asarray(audio, dtype=np.float32)
            audio_data = b""
            chunk = 4096
            for i in range(0,len(audio), chunk):
                frame = (audio[i:i+chunk]*32767).astype(np.int16, copy = False)
                audio_data += frame.tobytes()
        return audio_data

# Funcion sincrona (bloqueante)
    def write_audio_data(self, audio_data):
        length = len(audio_data)
        pos = 0
        while pos < length:
            if self.paused.is_set():
                print("TtS::break write_audio")
                clear_queue(self.text_queue)
                break
            end = pos + CHUNK
            data = audio_data[pos:end]

            print(".", end = "")
            self.audio_device.write(data)
            pos = end
        print()
        return pos

    def pause(self):
        self.paused.set()
        clear_queue(self.text_queue)
        print("TtS::pause(): ")

    def close(self):
        print("TtS::close()")
        self.pause()
        self.start_event.set()
        self.stop_event.set()
#        self.join()
        if(self.audio_device_type == "pyaudio"):
            self.audio_device.close
            self.p.terminate()

def clear_queue(q):
    while True:
        try:
            q.get_nowait()
            q.task_done()
        except queue.Empty:
            break