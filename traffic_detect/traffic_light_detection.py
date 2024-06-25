#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from bboxes_ex_msgs.msg import BoundingBox  # Import your custom message
import time

class StopRobotNode(Node):

    def __init__(self):
        super().__init__('stop_robot_node')
        self.subscription = self.create_subscription(
            BoundingBox,
            '/yolov5/bounding_box',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.get_logger().info('StopRobotNode has been started.')

    def listener_callback(self, msg):
        object_class = msg.class_
        if object_class == 'desired_object_type':  # Replace with your specific object type
            self.get_logger().info(f'Detected object: {object_class}. Stopping robot.')
            stop_msg = Twist()
            stop_msg.linear.x = 0.0
            stop_msg.angular.z = 0.0
            self.publisher.publish(stop_msg)
            time.sleep(4)  # Stop for 4 seconds
            self.get_logger().info('Resuming operation.')

def main(args=None):
    rclpy.init(args=args)
    node = StopRobotNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
