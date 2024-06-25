#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from bboxes_ex_msgs.msg import BoundingBoxes, BoundingBox  # Import your custom message
import time

class StopRobotNode(Node):

    def __init__(self):
        super().__init__('stop_robot_node')
        self.subscription = self.create_subscription(
            BoundingBoxes,
            'yolov5/bounding_boxes',
            self.listener_callback,
            10)
        self.goal_subscription = self.create_subscription(
            PoseStamped,
            'goal_pose',
            self.goal_callback,
            10)
        self.navigator = BasicNavigator()
        self.last_goal = None
        self.get_logger().info('StopRobotNode has been started.')

    def listener_callback(self, msg):
        
        bbox=BoundingBox()
        #self.get_logger().info('im in')
        for bbox in msg.bounding_boxes:
        #    msg=bboxes[i]
           # print(msg)
          #  dir(msg)
            object_class = bbox.class_id

            
            if object_class == 'traffic light':  # Replace with your specific object type
                self.get_logger().info(f'Detected object: {object_class}. Stopping robot.')
                self.cancel_goal()
                time.sleep(4)  # Stop for 4 seconds
                self.get_logger().info('Resuming operation.')
                self.replan_goal()
                break  # Stop processing after handling the first relevant bounding box

    def goal_callback(self, msg):
        self.last_goal = msg
        self.get_logger().info(f'Received new goal: {msg}')

    def cancel_goal(self):
        self.navigator.cancelTask()

    def replan_goal(self):
        if self.last_goal is not None:
            self.get_logger().info('Replanning to the last known goal.')
            poses = [self.last_goal]  # You can add multiple PoseStamped goals here for NavigateThroughPoses
            self.navigator.waitUntilNav2Active()
            self.navigator.goThroughPoses(poses)
            result = self.navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                self.get_logger().info('Goal succeeded!')
            elif result == TaskResult.CANCELED:
                self.get_logger().info('Goal was canceled!')
            elif result == TaskResult.FAILED:
                self.get_logger().info('Goal failed!')
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
