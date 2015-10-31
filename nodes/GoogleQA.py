#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file rosRTMdialogue.py
 @brief rosRTM
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import ROS module
import rospy

class GoogleQA(object):
    """ GoogleQA class """
    def __init__(self):
        """ Initializer """

    def run(self):
        """ run ros node """
        # initialize ros node
        rospy.init_node('GoogleQA')
 
        rospy.spin()


if __name__ == '__main__':
    try:
        node = GoogleQA()
        node.run()
    except rospy.ROSInterruptException:
        pass
