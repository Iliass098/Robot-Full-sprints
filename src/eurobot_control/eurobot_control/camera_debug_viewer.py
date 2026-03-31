#!/usr/bin/env python3

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image


class CameraDebugViewer(Node):
    def __init__(self):
        super().__init__('camera_debug_viewer')

        self.declare_parameter('track_topic', '/robot6/camera/image_raw')
        self.declare_parameter('mask_topic', '/robot6/debug/line_mask')
        self.declare_parameter('show_mask', True)
        self.declare_parameter('window_scale', 1.0)

        self.bridge = CvBridge()
        self.window_scale = max(float(self.get_parameter('window_scale').value), 0.1)
        self.track_window = 'Track Camera'
        self.mask_window = 'Line Mask'

        track_topic = str(self.get_parameter('track_topic').value)
        mask_topic = str(self.get_parameter('mask_topic').value)
        show_mask = bool(self.get_parameter('show_mask').value)

        self.create_subscription(Image, track_topic, self.track_callback, 10)
        if show_mask:
            self.create_subscription(Image, mask_topic, self.mask_callback, 10)

        cv2.namedWindow(self.track_window, cv2.WINDOW_NORMAL)
        if show_mask:
            cv2.namedWindow(self.mask_window, cv2.WINDOW_NORMAL)

        self.get_logger().info(
            f'Viewing {track_topic}'
            + (f' and {mask_topic}' if show_mask else '')
            + ' with OpenCV windows'
        )

    def track_callback(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        cv2.imshow(self.track_window, self._resize(frame))
        self._process_keys()

    def mask_callback(self, msg: Image):
        mask = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono8')
        cv2.imshow(self.mask_window, self._resize(mask))
        self._process_keys()

    def _resize(self, image):
        if self.window_scale == 1.0:
            return image
        return cv2.resize(
            image,
            None,
            fx=self.window_scale,
            fy=self.window_scale,
            interpolation=cv2.INTER_NEAREST,
        )

    def _process_keys(self):
        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord('q')):
            self.get_logger().info('Closing viewer on user request.')
            rclpy.shutdown()

    def destroy_node(self):
        cv2.destroyAllWindows()
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraDebugViewer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
