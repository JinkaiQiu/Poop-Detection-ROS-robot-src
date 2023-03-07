#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

"""
@作者: 古月居(www.guyuehome.com)
@说明: ROS2节点示例-通过摄像头识别检测图片中出现的苹果
"""

import rclpy                            # ROS2 Python接口库
from rclpy.node import Node             # ROS2 节点类

import cv2                              # OpenCV图像处理库
import numpy as np                      # Python数值计算库

lower_brown = np.array([0, 30, 70])     # Poop的HSV阈值下限
upper_brown = np.array([40, 225, 180])  # Poop的HSV阈值上限

def object_detect(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                       # 图像从BGR颜色模型转换为HSV模型
    mask_red = cv2.inRange(hsv_img, lower_brown, upper_brown)                  # 图像二值化

    contours, hierarchy = cv2.findContours(mask_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # 图像中轮廓检测

    for cnt in contours:                                                   # 去除一些轮廓面积太小的噪声
        if cnt.shape[0] < 500:
            continue
            
        (x, y, w, h) = cv2.boundingRect(cnt)                               # 得到苹果所在轮廓的左上角xy像素坐标及轮廓范围的宽和高
        cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)                 # 将苹果的轮廓勾勒出来
        cv2.circle(image, (int(x+w/2), int(y+h/2)), 5, (0, 255, 0), -1)    # 将苹果的图像中心点画出来
	    
    cv2.imshow("object", image)                                            # 使用OpenCV显示处理后的图像效果
    cv2.waitKey(500)

def main(args=None):                                                       # ROS2节点主入口main函数
    rclpy.init(args=args)                                                  # ROS2 Python接口初始化
    node = Node("node_object_webcam")                                      # 创建ROS2节点对象并进行初始化
    node.get_logger().info("ROS2节点示例：检测图像中的Poop")

    cap = cv2.VideoCapture(0)

    
    while rclpy.ok():
        ret, image = cap.read()          # 读取一帧图像
         
        if ret == True:
            object_detect(image)          # 苹果检测
        
    node.destroy_node()                  # 销毁节点对象
    rclpy.shutdown()                     # 关闭ROS2 Python接口
