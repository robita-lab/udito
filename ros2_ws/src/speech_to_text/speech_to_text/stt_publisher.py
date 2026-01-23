# DOA publishes Direction Of Audio source, and Voice Activity Detection (VAD) is a key part of the process.
# This code is a ROS2 node that publishes DOA and VAD data.

import usb.core
import usb.util
import time
import sys

import json
import io
import threading
import numpy as np
import queue
import pyaudio
import wave
import webrtcvad
import whisper
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from body_interfaces.msg import DOA
from body_interfaces.msg import Speech2Text

sys.path.append("/home/udito/OneDrive/UDITO/udito/src")
from audio.StT import StT

class StTPublisher(Node):

    def __init__(self):
        super().__init__('stt_publisher')
        self.doa_pub = self.create_publisher(DOA, 'doa_topic', 10)
        self.stt_pub = self.create_publisher(Speech2Text, 'stt_topic', 10)
        self.doa_msg = DOA()
        self.stt_msg = Speech2Text()
        self.stt = StT(self.result_callback, self.user_speaking)
        if self.stt.respeaker:
            self.get_logger().info('Mic found')
            self.stt.respeaker.set_vad_threshold( 50 )
        else:
            self.get_logger().error('Mic NOT found')
        self.stt.start()

    def result_callback(self, result):
            try:
                if len(result['results']) > 0:
                    self.stt_msg.text = result['results'][0]['alternatives'][0]['transcript'].strip()
                    self.stt_msg.confidence = result['results'][0]['alternatives'][0]['confidence']
                    self.stt_pub.publish(self.stt_msg)
                    self.get_logger().info('publishing text: %s,  conf:%f' %(self.stt_msg.text, self.stt_msg.confidence))
            except:
                self.get_logger().info('no result')  
                return None

    def user_speaking(self, flag):
        self.doa_msg.angle = self.stt.respeaker.direction
        self.doa_msg.vad = 1
        self.doa_msg.user_speaking = flag
        self.doa_pub.publish(self.doa_msg)
        self.get_logger().info('publishing user_speaking: "%d", angle:"%d", vad:%d' %(self.doa_msg.user_speaking, self.doa_msg.angle, self.doa_msg.vad))  


    def close(self):
        self.stt.close()

def main(args=None):
    rclpy.init(args=args)

    stt_pub = StTPublisher()
    try:
        rclpy.spin(stt_pub)
    except KeyboardInterrupt:
        print("StT::⏹️ Detenido por el usuario.")
    finally:
        stt_pub.close()
    stt_pub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()