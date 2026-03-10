from transitions import Machine
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time
import math
import json
from std_msgs.msg import String
from typing import Optional, Dict, Any
from std_msgs.msg import Bool
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

# ======================
# PARÁMETROS
# ======================

LINEAR_SPEED = 0.2
ANGULAR_SPEED = 0.6

LINE_LENGTH = 0.5
TURN_ANGLE = 144
RADIUS = 0.5

OBSTACLE_DISTANCE = 0.35
AVOID_TIME = 0.5
AVOID_TURN_SPEED = 0.8
AVOID_FORWARD_SPEED = 0.15


# ======================
# ROBOT CON FSM
# ======================

class StarRobot(Node):

    def __init__(self):
        super().__init__('star_robot_fsm')

        self.publisher_ = self.create_publisher(Twist, '/robot6/cmd_vel', 10)
        self.lidar_sub = self.create_subscription(LaserScan, '/robot6/scan', self.lidar_callback, 10)

        self.obstacle_detected = False

        #aruco parte

        self.bridge = CvBridge()
        self.aruco_detected = False

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters_create()

        self.create_subscription(Image,'/robot6/camera/image_raw',self.camera_callback,10)

    # ----------------------
    # LIDAR
    # ----------------------
    def lidar_callback(self, msg: LaserScan):

    # Calcular índice del ángulo 0 (frente real)
        center_index = int((0.0 - msg.angle_min) / msg.angle_increment)

    # Queremos ±20 grados
        angle_range_deg = 20
        angle_range_rad = math.radians(angle_range_deg)

        delta = int(angle_range_rad + 180 / msg.angle_increment)

        start = max(0, center_index - delta)
        end = min(len(msg.ranges), center_index + delta)

        front_ranges = msg.ranges[start:end]

        valid_ranges = [r for r in front_ranges 
                    if msg.range_min < r < msg.range_max]

        if not valid_ranges:
            return

        min_distance = min(valid_ranges)

        if min_distance < OBSTACLE_DISTANCE:
            self.get_logger().warn(f"OBSTÁCULO a {min_distance:.2f} m")
            self.obstacle_detected = True
        else:
            self.obstacle_detected = False

    # ----------------------
    # MOVIMIENTOS
    # ----------------------
    def draw_line(self):
        self.get_logger().info("Avanzando línea")
        msg = Twist()
        msg.linear.x = LINEAR_SPEED

        start = time.time()
        duration = LINE_LENGTH / LINEAR_SPEED

        while time.time() - start < duration:
            rclpy.spin_once(self, timeout_sec=0.01)

            if self.obstacle_detected:
                return

            self.publisher_.publish(msg)

        self.stop_robot()

    def turn(self):
        self.get_logger().info("Girando")
        msg = Twist()
        msg.angular.z = ANGULAR_SPEED

        duration = math.radians(TURN_ANGLE) / ANGULAR_SPEED
        start = time.time()

        while time.time() - start < duration:
            rclpy.spin_once(self, timeout_sec=0.01)

            if self.obstacle_detected:
                return

            self.publisher_.publish(msg)

        self.stop_robot()

    def draw_circle(self):
        self.get_logger().info("Dibujando círculo")
        msg = Twist()
        msg.linear.x = LINEAR_SPEED
        msg.angular.z = LINEAR_SPEED / RADIUS

        duration = (2 * math.pi * RADIUS) / LINEAR_SPEED
        start = time.time()

        while time.time() - start < duration:
            rclpy.spin_once(self, timeout_sec=0.01)

            if self.obstacle_detected:
                return

            self.publisher_.publish(msg)

        self.stop_robot()
    # ----------------------
    # AVOIDANCE
    # ----------------------
    def avoid_obstacle(self):
        self.get_logger().warn("EVADIENDO OBSTÁCULO")

        msg = Twist()

    # 1️⃣ Girar hasta liberar el frente
        msg.linear.x = 0.0
        msg.angular.z = AVOID_TURN_SPEED

        while self.obstacle_detected:
            rclpy.spin_once(self, timeout_sec=0.01)
            self.publisher_.publish(msg)

        self.stop_robot()

    # 2️⃣ Avanzar un poco para esquivar
        msg.angular.z = 0.0
        msg.linear.x = AVOID_FORWARD_SPEED

        start = time.time()
        while time.time() - start < 1.0:
            rclpy.spin_once(self, timeout_sec=0.01)
            self.publisher_.publish(msg)

        self.stop_robot()

    def stop_robot(self):
        self.publisher_.publish(Twist())
        time.sleep(0.5)

#----------
#ARUCO
#--------

    def camera_callback(self, msg):

        if self.aruco_detected:
            return

        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.aruco_params)

        if ids is not None:
            for marker_id in ids.flatten():
                if marker_id == 20:
                    self.get_logger().info("Aruco objetivo detectado")
                    self.aruco_detected = True
# ======================
# MAIN
# ======================

def main():
    rclpy.init()
    robot = StarRobot()

    states = [
        'line1', 'line2', 'line3',
        'line4', 'line5',
        'circle', 'avoidance', 'finished', 'girando'
    ]

    machine = Machine(model=robot, states=states, initial='line1')

    machine.add_transition('next', 'line1', 'line2', after=['draw_line', 'turn'])
    machine.add_transition('next', 'line2', 'line3', after=['draw_line', 'turn'])
    machine.add_transition('next', 'line3', 'line4', after=['draw_line', 'turn'])
    machine.add_transition('next', 'line4', 'line5', after=['draw_line', 'turn'])
    machine.add_transition('next', 'line5', 'circle', after='draw_line')
    machine.add_transition('next', 'circle', 'girando', after='draw_circle')
    machine.add_transition('next', 'girando', 'girando', after='turn')
    
    
    machine.add_transition('to_avoidance', 'line1', 'avoidance')
    machine.add_transition('to_avoidance', 'line2', 'avoidance')
    machine.add_transition('to_avoidance', 'line3', 'avoidance')
    machine.add_transition('to_avoidance', 'line4', 'avoidance')
    machine.add_transition('to_avoidance', 'line5', 'avoidance')
    machine.add_transition('to_avoidance', 'circle', 'avoidance')
    machine.add_transition('recover', 'avoidance', 'line1')

    machine.add_transition('aruco20_seen', '*', 'finished')

    # 👉 Hilo de ejecución ROS
    executor = rclpy.executors.SingleThreadedExecutor()
    executor.add_node(robot)

    try:
        while rclpy.ok() and robot.state != 'finished':

            executor.spin_once(timeout_sec=0.01)
            
            #girando giando girand girado
            if robot.state == 'girando':
                robot.get_logger().info("Figura completada")

            # Si detecta obstáculo → avoidance
            if robot.obstacle_detected and robot.state != 'avoidance' and robot.state != 'girando':
                robot.stop_robot()
                robot.to_avoidance()
                robot.avoid_obstacle()
                robot.recover()
                continue
            
            if robot.aruco_detected:
                robot.stop_robot()
                robot.aruco20_seen()
                robot.get_logger().info("Aruco detectado -> deteniendo robot")
            else:
                robot.next()

        robot.stop_robot()


    finally:
        robot.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    main()