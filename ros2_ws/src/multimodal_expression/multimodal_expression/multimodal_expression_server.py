from body_interfaces.srv import ComActMsg

import rclpy
from rclpy.node import Node 
import sys
sys.path.append("/home/udito/OneDrive/UDITO/udito/src/audio")
from ComAct import ComAct
from body_interfaces.msg import RobotSpeaking

class ComActService(Node):
    def __init__(self):
        super().__init__('com_act_server')
        self.srv = self.create_service(ComActMsg, 'com_act_server', self.com_act_callback)
        self.robot_speaking_pub = self.create_publisher(RobotSpeaking, "robot_speaking_topic", 10)
        self.robot_speaking_msg = RobotSpeaking()
        self.myComAct = ComAct(robot_speaking_callback = self.robot_speaking)
        self.myComAct.speak("Servicio de comunicación activo!", "HAPPY", 5)

    def com_act_callback(self, request, response):
        self.get_logger().info('Server received\ncmd: %s text: %s gesture: %s gesture_parameter: %d' % (request.cmd, request.text, request.gesture, request.data))
        if request.cmd == "speak":
            self.myComAct.speak(request.text, request.gesture, request.data)
            response.rta = "ACK"
        elif request.cmd == "shut_up":
            self.myComAct.pause()
            response.rta = "ACK"
        else:
            response.rta = "ERROR"
        return response

    def robot_speaking(self, flag):
        self.robot_speaking_msg.robot_speaking = flag
        self.robot_speaking_pub.publish(self.robot_speaking_msg)
        self.get_logger().info('publishing.robot_speaking: "%r"' %(self.robot_speaking_msg.robot_speaking))

def main():
    rclpy.init()
    com_act_service = ComActService()
    rclpy.spin(com_act_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
