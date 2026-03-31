#!/usr/bin/env python3

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Image


class LineFollowerNode(Node):
    def __init__(self):
        super().__init__('line_follower')

        self.declare_parameter('camera_topic', '/robot6/camera/image_raw')
        self.declare_parameter('cmd_vel_topic', '/robot6/cmd_vel')
        self.declare_parameter('debug_image_topic', '/robot6/debug/line_mask')
        self.declare_parameter('line_color', 'black')
        self.declare_parameter('roi_top_fraction', 0.60)
        self.declare_parameter('base_speed', 0.12)
        self.declare_parameter('reduced_speed', 0.05)
        self.declare_parameter('max_angular', 1.5)
        self.declare_parameter('kp', 0.0045)
        self.declare_parameter('ki', 0.0002)
        self.declare_parameter('kd', 0.0020)
        self.declare_parameter('integral_limit', 3000.0)
        self.declare_parameter('min_contour_area', 700.0)
        self.declare_parameter('lost_stop', True)
        self.declare_parameter('publish_debug_image', True)

        self.bridge = CvBridge()
        self.prev_error = 0.0
        self.integral = 0.0
        self.last_stamp = None

        camera_topic = self.get_parameter('camera_topic').value
        cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        debug_topic = self.get_parameter('debug_image_topic').value

        self.cmd_pub = self.create_publisher(Twist, cmd_vel_topic, 10)
        self.debug_pub = self.create_publisher(Image, debug_topic, 10)
        self.image_sub = self.create_subscription(
            Image,
            camera_topic,
            self.image_callback,
            10,
        )

        self.get_logger().info(
            f'Line follower listening on {camera_topic} and publishing to {cmd_vel_topic}'
        )

    def image_callback(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        height, width = frame.shape[:2]
        roi_top_fraction = float(self.get_parameter('roi_top_fraction').value)
        roi_top = int(height * roi_top_fraction)
        roi = frame[roi_top:, :]

        if roi.size == 0:
            return

        mask = self._build_mask(roi)
        centroid_x = self._get_centroid(mask)

        if bool(self.get_parameter('publish_debug_image').value):
            self.debug_pub.publish(self.bridge.cv2_to_imgmsg(mask, encoding='mono8'))

        if centroid_x is None:
            self.integral = 0.0
            if bool(self.get_parameter('lost_stop').value):
                self.cmd_pub.publish(Twist())
            return

        center_x = width / 2.0
        error = float(centroid_x - center_x)
        dt = self._compute_dt()

        kp = float(self.get_parameter('kp').value)
        ki = float(self.get_parameter('ki').value)
        kd = float(self.get_parameter('kd').value)
        integral_limit = float(self.get_parameter('integral_limit').value)
        max_angular = float(self.get_parameter('max_angular').value)

        self.integral += error * dt
        self.integral = float(np.clip(self.integral, -integral_limit, integral_limit))
        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        angular = -(kp * error + ki * self.integral + kd * derivative)
        angular = float(np.clip(angular, -max_angular, max_angular))

        base_speed = float(self.get_parameter('base_speed').value)
        reduced_speed = float(self.get_parameter('reduced_speed').value)
        turn_ratio = min(abs(angular) / max_angular, 1.0) if max_angular > 0.0 else 1.0
        linear = base_speed - (base_speed - reduced_speed) * turn_ratio

        cmd = Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        self.cmd_pub.publish(cmd)

    def _build_mask(self, roi: np.ndarray) -> np.ndarray:
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        line_color = str(self.get_parameter('line_color').value).lower()

        if line_color == 'white':
            lower = np.array([0, 0, 200], dtype=np.uint8)
            upper = np.array([180, 30, 255], dtype=np.uint8)
        else:
            lower = np.array([0, 0, 0], dtype=np.uint8)
            upper = np.array([180, 255, 40], dtype=np.uint8)

        mask = cv2.inRange(hsv, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        return mask

    def _get_centroid(self, mask: np.ndarray):
        moments = cv2.moments(mask)
        min_contour_area = float(self.get_parameter('min_contour_area').value)
        if moments['m00'] < min_contour_area:
            return None
        return int(moments['m10'] / moments['m00'])

    def _compute_dt(self) -> float:
        now = self.get_clock().now()
        if self.last_stamp is None:
            dt = 1.0 / 30.0
        else:
            dt = (now - self.last_stamp).nanoseconds * 1e-9
            dt = max(dt, 1e-4)
        self.last_stamp = now
        return dt


def main(args=None):
    rclpy.init(args=args)
    node = LineFollowerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
