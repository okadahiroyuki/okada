#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
    背景差分で動きを検出する

    The project is hosted on GitHub where your could fork the project or report
    issues. Visit https://github.com/roboworks/

    :copyright: (c) 2015 by Hiroyuki Okada, All rights reserved.
    :license: MIT License (MIT), http://www.opensource.org/licenses/MIT
"""
__author__ = 'Hiroyuki Okada'
__version__ = '0.1'
import rospy
import sys
import cv2
import cv2.cv as cv
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from numpy import *
import os.path
import time

# 背景差分
#def bg_diff(fn_bg,im_in,th,blur):
def bg_diff(fn_bg,im_in,th,blur):    
    # 背景, 入力画像の取得
#    im_bg = cv2.imread(fn_bg,0);    
    im_bg = fn_bg
    # 差分計算
    diff = cv2.absdiff(im_in,im_bg)
    # 差分が閾値より小さければTrue
    mask = diff < th
    # 配列（画像）の高さ・幅
    hight = im_bg.shape[0]
    width = im_bg.shape[1]
    # 背景画像と同じサイズの配列生成
    im_mask = np.zeros((hight,width),np.uint8)
    # Trueの部分（背景）は白塗り
    im_mask[mask]=255
    # ゴマ塩ノイズ除去
    im_mask = cv2.medianBlur(im_mask,blur)
    # エッジ検出
    im_edge = cv2.Canny(im_mask,100,200)

    return im_bg, im_in, im_mask, im_edge


def nothing(x):
    pass

class cvBridgeDemo():
    def __init__(self):
        self.node_name = "cv_bridge_demo"
        
        rospy.init_node(self.node_name)
        
        # What we do during shutdown
        # シャットダウンの時の処理
        rospy.on_shutdown(self.cleanup)

        # 閾値調整用のスライダー生成
        cv2.namedWindow("Motion Edge")
        cv2.createTrackbar("threshold", "Motion Edge", 60, 255, nothing)

        # 画像の差分を計算するために一回目の処理かどうかを知るため
        self.isStart = True

        
        # Create the OpenCV display window for the RGB image
        # RGB 画像のための表示ウィンドウの作成
        self.cv_window_name = self.node_name
        cv.NamedWindow(self.cv_window_name, cv.CV_WINDOW_NORMAL)
        cv.MoveWindow(self.cv_window_name, 25, 75)
        
        # And one for the depth image
        # 距離 画像のための表示ウィンドウの作成
        cv.NamedWindow("Depth Image", cv.CV_WINDOW_NORMAL)
        cv.MoveWindow("Depth Image", 25, 350)
        
        # Create the cv_bridge object
        # cv_bridge（OpenCVとROSの相互変換のための） オブジェクトの作成
        self.bridge = CvBridge()

        

        # Subscribe to the camera image and depth topics and set
        # the appropriate callbacks
        # RGB画像，距離画像を購読するコールバック関数の登録
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.image_callback, queue_size=1)
#        self.image_sub = rospy.Subscriber("input_rgb_image", Image, self.image_callback, queue_size=1)
        self.depth_sub = rospy.Subscriber("/camera/depth_registered/image_raw", Image, self.depth_callback, queue_size=1)
#        self.depth_sub = rospy.Subscriber("input_depth_image", Image, self.depth_callback, queue_size=1)        
        
        rospy.loginfo("Waiting for image topics...")
        rospy.wait_for_message("input_rgb_image", Image)
        rospy.wait_for_message("input_depth_image", Image)		
        rospy.loginfo("Ready.")

        
	# RGB画像が配信されると呼ばれる関数        
    def image_callback(self, ros_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
		# cv_bridge() で ROS image を OpenCV formatに変換する
        try:
            frame = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")
        except CvBridgeError, e:
            print e
        
        # Convert the image to a numpy array since most cv2 functions
        # require numpy arrays.
        # frame = np.array(frame, dtype=np.uint8)
        

        # Process the frame using the process_image() function
        # display_image = self.process_image(frame)
        # RGB画像を使った処理を行う関数を呼ぶ
		# メインの処理はここに書く
        # 取得した映像をグレースケール変換
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow(self.node_name, frame)            
        th = cv2.getTrackbarPos("threshold", "Motion Edge")
        if self.isStart == True:
            print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            self.isStart = False
            self.frame_prev=frame
        else:
            im_bg,im_in,im_mask,im_edge = bg_diff(self.frame_prev,frame,th,blur=7)
            cv2.imshow("Input",im_in)
            cv2.imshow("Background",im_bg)
            cv2.imshow("Motion Edge",im_edge)










        
        # Display the image.
        #cv2.imshow(self.node_name, display_image)
#        cv2.imshow(self.node_name, frame)
        #差分用に一回前の画像を保存しておく
        self.frame_prev = frame
        
        # Process any keyboard commands
        self.keystroke = cv2.waitKey(5)
        if self.keystroke != -1:
            cc = chr(self.keystroke & 255).lower()
            if cc == 'q':
                # The user has press the q key, so exit
                rospy.signal_shutdown("User hit q key to quit.")

                
    def depth_callback(self, ros_image):
        # Use cv_bridge() to convert the ROS image to OpenCV format
        try:
            # Convert the depth image using the default passthrough encoding
            depth_image = self.bridge.imgmsg_to_cv2(ros_image, "passthrough")
        except CvBridgeError, e:
            print e

        # Convert the depth image to a Numpy array since most cv2 functions require Numpy arrays.
        depth_array = np.array(depth_image, dtype=np.float32)
                
        # Normalize the depth image to fall between 0 (black) and 1 (white)
        cv2.normalize(depth_array, depth_array, 0, 1, cv2.NORM_MINMAX)
        
        # Process the depth image
        depth_display_image = self.process_depth_image(depth_array)
    
        # Display the result
        cv2.imshow("Depth Image", depth_display_image)

    # RGB画像を使った処理を行う          
    def process_image(self, frame):
        # Convert to greyscale
        # グレイスケールへの変換
        grey = cv2.cvtColor(frame, cv.CV_BGR2GRAY)
        
        # Blur the image
        grey = cv2.blur(grey, (7, 7))
        
        # Compute edges using the Canny edge filter
        edges = cv2.Canny(grey, 15.0, 30.0)
        
        return edges

    # 距離画像を使った処理を行う        
    def process_depth_image(self, frame):
        # Just return the raw image for this demo
        return frame

    # シャットダウンのときの処理    
    def cleanup(self):
        print "Shutting down vision node."
        cv2.destroyAllWindows()   
    
def main(args):       
    try:
        cvBridgeDemo()
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down vision node."
        cv.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)








    
