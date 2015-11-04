#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-
"""
    DoCoMoChatSrv.py


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
from okada.msg import DoCoMoChatRes
from okada.msg import DoCoMoChatReq
from okada.srv import DoCoMoChat
from okada.srv import DoCoMoChatResponse
import urllib2
import urllib
import json

class DoCoMoChatSrv(object):
    """ DoCoMoChatSrv class """
    def __init__(self):
        """ Initializer """

    def run(self):
        """ run ros node """
        # initialize ros node
        rospy.init_node('docomoChat')
        rospy.loginfo("start DoCoMoChat node")

        service_server = rospy.Service('docomo_chat', DoCoMoChat, self.Chat_handler)
        rospy.loginfo("start DoCoMoChat service server")

        self.url = rospy.get_param("~chat_url", "https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue")
        self.APIKEY = rospy.get_param("~APIKEY", "4e4e61744672324d792f533965647867467767654978717445316a3337696430386b453371715246456238")

        self.api_url = self.url + '?APIKEY=%s'%(self.APIKEY)

        
        rospy.spin()

    def Chat_handler(self,  query):
        req = query.request
        rospy.loginfo("DoCoMoChat :%s", req.utt)
        rospy.loginfo("DoCoMoChat :%s", req.context)

        req_data ={}
        req_data['utt'] = req.utt
        req_data['context'] = req.context
        print req_data

        req = urllib2.Request(self.api_url, json.dumps(req_data))
        req.add_header('Content-Type', 'application/json')
        try:
            res = urllib2.urlopen(req)
        except Exception as e:
            print e
            sys.exit()

        resp_json = json.load(res)
        self.context = resp_json['context'].encode('utf-8')
        self.mode    = resp_json['mode'].encode('utf-8')
        print resp_json['utt'].encode('utf-8')


            

        return
        
if __name__ == '__main__':
    try:
        node = DoCoMoChatSrv()
        node.run()
    except rospy.ROSInterruptException:
        pass
