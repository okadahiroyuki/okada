#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-
"""
    Chat program

    ROSPEEXから入力された文章
    The project is hosted on GitHub where your could fork the project or report
    issues. Visit https://github.com/roboworks/

    :copyright: (c) 2015 by Hiroyuki Okada, All rights reserved.
    :license: MIT License (MIT), http://www.opensource.org/licenses/MIT
"""
import sys
import time
sys.path.append(".")

import rospy
from std_msgs.msg import String
from rospeex_if import ROSpeexInterface
from okada.srv import QaQuery
import urllib2
import urllib
import json

class ChatTRCP(object):
    """ ChatTRCP class """
    def __init__(self):
        """ Initializer """

    def run(self):
        """ run ros node """
        # initialize ros node
        rospy.init_node('ChatTRCP')

        """ DoCoMo知識Q&A """
        self.docomo_qa = rospy.ServiceProxy('docomo_qa', QaQuery)



        
        rospeex = ROSpeexInterface()
        rospeex.init()
        rospeex.register_sr_response( self.sr_response )
        rospeex.set_spi_config(language='ja',engine='nict')

        rospy.spin()

    def sr_response(self, message):
        rospy.loginfo("sr_responsee:%s", message)


        """ DoCoMo知識Q&A """
        try:
            ret = self.docomo_qa(message)
            if ret.success:
                rospy.loginfo("DoCoMoQa Response:%s", ret.response)
            else:
                rospy.loginfo("DoCoMoQa Response:failed")            
        except:
            pass



            
if __name__ == '__main__':
    try:
        node = ChatTRCP()
        node.run()
    except rospy.ROSInterruptException:
        pass
