#
# pip install ibm-watsonx-ai
#

from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods

import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from body_interfaces.msg import DOA
from body_interfaces.msg import Speech2Text
from body_interfaces.srv import Text2Speech
from body_interfaces.srv import ComActMsg
import sys 
sys.path.append("/home/udito/OneDrive/UDITO/udito/src/audio")
from watsonAPI import Watson

class DMS(Node):
    def __init__(self):
        super().__init__('dms_node')
        self.watson = Watson()

        self.stt_sub = self.create_subscription(
            Speech2Text,
            'stt_topic',
            self.stt_callback,
            10)

        self.doa_sub = self.create_subscription(
            DOA,
            'doa_topic',
            self.doa_callback,
            10)

        self.cli = self.create_client(ComActMsg, 'com_act_server')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = ComActMsg.Request()

    def send_request(self, text, gesture, gesture_parameter, cmd = "speak"):
        self.req.cmd = cmd
        self.req.text = text
        self.req.gesture = gesture
        self.req.data = gesture_parameter
        return self.cli.call_async(self.req)
    
    def service_response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info('Respuesta del servicio:%s' %response.rta)
        except Exception as e:
            self.get_logger().error(f'Error al llamar al servicio: {e}')

    def stt_callback(self,msg):
        self.get_logger().info('received: %s, conf: %f' %(msg.text, msg.confidence))
        # expresion no verbal "pensando..."
        if msg.confidence > 0.6:
            self.send_request("oh", "NEUTRAL", 7, cmd = "speak")
            self.send_request("e", "BLINK", 10, cmd = "speak")
            self.send_request("pensando...", "ANGRY", 7, cmd="shut_up")
            self.prompt = msg.text
        else:
            self.send_request("repítelo", "NEUTRAL", 10)
            self.promt = None
            return 
        response = self.watson.generate_text(self.prompt)
        self.get_logger().info('watson says: %s' %response)
        self.send_request(response, "NO", 7)
        self.send_request("", "SURPRISED", 10)

    def doa_callback(self,msg):
        self.send_request("si", "LOVE", 10, cmd = "speak")


def main():
    print('Hi from watson_dialog_manager.')
    rclpy.init()

    minimal_subscriber = DMS()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
