# Communicative Multimodal Act
# 
import time
import threading
from playsound import playsound

from TtS import TtS

import sys
sys.path.append("/home/udito/OneDrive/UDITO/udito/src/head")
from headClass import Head

# TODO: Hacer la cola de texto en esta clase y no en TtS para poder coordinar mejor gestos y voz

class ComAct:
    def __init__(self, robot_speaking_callback = None):
        print("ComAct::ctor")
        self.head = Head()
        self.tts = TtS(robot_speaking_callback)
        #TODO: esperar a los constructoras y hebras activas
        time.sleep(3)
#        print("ComAct::waiting Head...")
#        while self.head.active

    def pause(self):
        self.tts.pause()
        self.head.pause()

    def show_gesture(self, gesture, gesture_parameter):
        self.head.start_event.set()
#        self.tts.start_event.set()
        self.head.act(gesture, gesture_parameter)
        self.head.done_event.wait()
#        self.tts.done_event.wait()

    def speak(self, text):
        self.speak(text, "NEUTRAL", 5)

    def speak(self, text, gesture = "NEUTRAL", gesture_parameter = 5):
        self.tts.speak(text)
        self.head.act(gesture, gesture_parameter)

        self.tts.activate()
        self.head.start_event.set()

        self.tts.wait_until_done()
        self.head.done_event.wait()

    def non_verbal_expression(self, gesture, gesture_parameter):
        sound_file = "./samples/whistle-short-01.wav"
        if gesture == "ANGRY":
            sound_file = "./samples/angry_lion.wav"
        elif gesture == "LOVE":
            sound_file = "./samples/i_love_you.mp3"
        elif gesture == "LAUGH":
            sound_file = "./samples/laughing_girls.wav"
        elif gesture == "SAD":
            sound_file = "./samples/SadR2D2.mp3"
        elif gesture == "HAPPY":
            sound_file = "./samples/ExcitedR2D2.mp3"
        elif gesture == "SURPRISED":
            sound_file = "./samples/cat_meow.mp3"
        elif gesture == "NEUTRAL":
            sound_file = "./samples/WhistleAttention.wav"
        elif gesture == "BLINK":
            sound_file = "./samples/whistle-short-01.wav"
        elif gesture == "WINK":
            sound_file = "./samples/whistle_sexy.wav"
        elif gesture == "YES":
            sound_file = "./samples/LookR2D2.mp3"
        elif gesture == "NO":
            sound_file = "./samples/SnappyR2D2.mp3"

        self.head.act(gesture, gesture_parameter)
        playsound(sound_file)

    def close(self):
        print("ComAct::close")
        self.tts.close()
        self.head.close()
