#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-
"""
    DoCoMoQA.py


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
from okada.srv import QaQueryResponse
import urllib2
import urllib
import json

class DoCoMoQA(object):
    """ DoCoMoQA class """
    def __init__(self):
        """ Initializer """

    def run(self):
        """ run ros node """
        # initialize ros node
        rospy.init_node('docomo')
        rospy.loginfo("start DoCoMoQA node")

        service_server = rospy.Service('docomo_qa', QaQuery, self.Qa_handler)
        rospy.loginfo("start DoCoMoQA service server")

        self.url = rospy.get_param("~qa_url", "https://api.apigw.smt.docomo.ne.jp/knowledgeQA/v1/ask?")
        self.APIKEY = rospy.get_param("~APIKEY", "4e4e61744672324d792f533965647867467767654978717445316a3337696430386b453371715246456238")

        
        rospy.spin()

    def Qa_handler(self, query):
        rospy.loginfo("DoCoMoQa Query:%s", query.data)
        msg = {}
        msg['APIKEY'] = self.APIKEY
        msg['q'] = query.data

        url_value = urllib.urlencode(msg)
        req = urllib2.Request(self.url+url_value)
        try:
            response = urllib2.urlopen(req)
        except Exception as e:
            print e
            return QaQueryResponse(success=False)
        else:
            the_page = json.loads(response.read())
            msg=the_page['message']
            res=msg['textForSpeech']
            rospy.loginfo("DoCoMoQa Response:%s", res)
            return QaQueryResponse(success=True, response=res)
        
if __name__ == '__main__':
    try:
        node = DoCoMoQA()
        node.run()
    except rospy.ROSInterruptException:
        pass
