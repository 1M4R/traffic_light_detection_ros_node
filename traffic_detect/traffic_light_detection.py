#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from bboxes_ex_msgs.msg import BoundingBoxes, BoundingBox, ObjectCount  # Import your custom message
import time

class StopRobotNode(Node):

    def __init__(self):
        super().__init__('stop_robot_node')
        self.subscription = self.create_subscription(
            BoundingBoxes,
            'yolov5/bounding_boxes',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.get_logger().info('StopRobotNode has been started.')

    def listener_callback(self, msg):
        
        bboxes = BoundingBoxes.bounding_boxes
        msg=BoundingBox()
       # self.get_logger().info()
        for i in range(1):
            msg=bboxes[i]
            print(msg)
            dir(msg)
            object_class = msg.class_id[i]

            print(object_class)
            self.get_logger().info('im in2')
            if object_class == 'traffic light':  # Replace with your specific object type
                self.get_logger().info(f'Detected object: {object_class}. Stopping robot.')
                stop_msg = Twist()
                stop_msg.linear.x = 0.0
                stop_msg.angular.z = 0.0
                self.publisher.publish(stop_msg)
                time.sleep(4)  # Stop for 4 seconds
                self.get_logger().info('Resuming operation.')
            i+=1
        return None

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
