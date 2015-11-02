#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ChatDoCoMoAPI.py
 @brief 
 @date $Date$


"""
import sys
import time
sys.path.append(".")

import rospy
from std_msgs.msg import String
from rospeex_if import ROSpeexInterface

import urllib2
import urllib
import json

url = 'https://api.apigw.smt.docomo.ne.jp/knowledgeQA/v1/ask?'
APIKEY = '4e4e61744672324d792f533965647867467767654978717445316a3337696430386b453371715246456238'

class GoogleQA(object):
    """ GoogleQA class """
    def __init__(self):
        """ Initializer """

    def run(self):
        """ run ros node """
        # initialize ros node
        rospy.init_node('GoogleQA')
 
        rospeex = ROSpeexInterface()
        rospeex.init()
        rospeex.register_sr_response( self.sr_response )
        rospeex.set_spi_config(language='ja',engine='nict')


	self.data = {}
	self.data['APIKEY'] = APIKEY
        rospy.spin()

    def sr_response(self, message):
	print message 
	self.data['q'] = message 

	try:
	    url_value = urllib.urlencode(self.data)
	    req = urllib2.Request(url+url_value)
	    response = urllib2.urlopen(req)
	    the_page = json.loads(response.read())
	    a=the_page['message']
	    print a['textForSpeech']
	except:
	    pass


if __name__ == '__main__':
    try:
        node = GoogleQA()
        node.run()
    except rospy.ROSInterruptException:
        pass
